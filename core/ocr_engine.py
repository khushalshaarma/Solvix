import logging
import re
import cv2  # type: ignore[import]
import numpy as np
import pytesseract
from mss import mss  # type: ignore[import]
from PIL import Image
from PyQt6.QtCore import QObject, QTimer, pyqtSignal  # type: ignore[import]

logger = logging.getLogger(__name__)


class OCREngine(QObject):
    text_captured = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, tesseract_path=None):
        super().__init__()
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.sct = mss()
        self.last_text = ""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        logger.info("[OCR] Engine initialized with sequential reading")

    def capture_region(self, left_pct=0.05, top_pct=0.08, width_pct=0.90, height_pct=0.85):
        """Capture a configurable region - defaults to center 90% width, 85% height
        to exclude browser chrome but capture the exam content area."""
        mon = self.sct.monitors[1]
        w, h = mon["width"], mon["height"]
        region = {
            "left": mon["left"] + int(w * left_pct),
            "top": mon["top"] + int(h * top_pct),
            "width": int(w * width_pct),
            "height": int(h * height_pct),
        }
        img = np.array(self.sct.grab(region))
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img

    @staticmethod
    def preprocess(img: np.ndarray) -> np.ndarray:
        """Enhanced preprocessing for better OCR accuracy on exam text."""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Increase contrast
        gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        # Sharpen
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharp = cv2.filter2D(denoised, -1, kernel)
        # Binary threshold
        _, thresh = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def extract_question_blocks(self, img: np.ndarray) -> list:
        """Extract individual question blocks using bounding box analysis.
        Returns list of (question_number, text) tuples in reading order (top-to-bottom)."""
        processed = self.preprocess(img)
        
        # Get word-level bounding boxes with confidence
        data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
        
        # Group words into lines based on y-coordinate proximity
        lines = []
        current_line = []
        current_y = None
        y_threshold = 15  # pixels tolerance for same line
        
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])
            if not text or conf < 30:
                continue
            
            x = data['left'][i]
            y = data['top'][i]
            
            if current_y is None:
                current_y = y
                current_line = [(x, y, text)]
            elif abs(y - current_y) <= y_threshold:
                current_line.append((x, y, text))
            else:
                # Sort words left-to-right, join them
                current_line.sort(key=lambda w: w[0])
                line_text = " ".join(w[2] for w in current_line)
                lines.append((current_y, line_text))
                current_y = y
                current_line = [(x, y, text)]
        
        if current_line:
            current_line.sort(key=lambda w: w[0])
            line_text = " ".join(w[2] for w in current_line)
            lines.append((current_y, line_text))
        
        # Sort lines top-to-bottom
        lines.sort(key=lambda l: l[0])
        
        # Try to detect question boundaries (look for numbers followed by dot, period, or )
        questions = []
        current_q = []
        q_num = 0
        
        q_pattern = re.compile(r'^(\d+)[\.\)]\s*')
        
        for y, text in lines:
            match = q_pattern.match(text)
            if match:
                # Save previous question
                if current_q:
                    questions.append((q_num, " ".join(current_q)))
                q_num = int(match.group(1))
                current_q = [text]
            else:
                # Check for answer options (A), B), C), D))
                opt_match = re.match(r'^([A-Da-d])[\)\.]\s+', text)
                if opt_match or text.strip():
                    current_q.append(text)
        
        # Don't forget the last question
        if current_q:
            questions.append((q_num, " ".join(current_q)))
        
        return questions

    def capture_and_ocr(self) -> str:
        """Full capture and OCR, returning the most recent complete question."""
        img = self.capture_region()
        if img is None:
            return ""
        
        questions = self.extract_question_blocks(img)
        
        if not questions:
            # Fallback: just get all text
            processed = self.preprocess(img)
            text = pytesseract.image_to_string(processed).strip()
            if len(text) > 15:
                return text
            return ""
        
        # Return the last complete question (most recently visible)
        last_q_num, last_q_text = questions[-1]
        
        # Also include context: the question number and surrounding options
        # This gives the AI the full question context
        full_text = []
        for qn, qt in questions[-2:] if len(questions) >= 2 else questions:
            full_text.append(qt)
        
        result = "\n".join(full_text)
        logger.info(f"[OCR] Extracted Q{last_q_num} ({len(result)} chars)")
        return result

    def capture_all_questions(self) -> str:
        """Capture all visible questions on screen (for initial scan)."""
        img = self.capture_region()
        if img is None:
            return ""
        questions = self.extract_question_blocks(img)
        if not questions:
            processed = self.preprocess(img)
            return pytesseract.image_to_string(processed).strip()
        return "\n---\n".join(f"Q{qn}: {qt}" for qn, qt in questions)

    def start_auto_capture(self, interval_ms=2500):
        self._timer.start(interval_ms)
        logger.info(f"[OCR] Auto-capture started ({interval_ms}ms)")

    def stop_auto_capture(self):
        self._timer.stop()

    def _tick(self):
        text = self.capture_and_ocr()
        if text and text != self.last_text and len(text) > 15:
            self.last_text = text
            logger.info(f"[OCR] New question detected ({len(text)} chars)")
            self.text_captured.emit(text)
