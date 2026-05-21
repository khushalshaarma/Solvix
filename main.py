#!/usr/bin/env python3
"""CoCubes Exam Assistant v2 - Sequential question reader + rich UI."""
import logging, os, sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("assistant.log", "w"), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def main():
    from config import config
    from core.ai_engine import AIEngine
    from core.ocr_engine import OCREngine
    from ui.stealth_window import StealthWindow
    from PyQt6.QtWidgets import QApplication  # type: ignore[import]
    from PyQt6.QtGui import QPalette, QColor  # type: ignore[import]
    from PyQt6.QtCore import QTimer  # type: ignore[import]

    app = QApplication(sys.argv)
    app.setApplicationName("System Helper")
    app.setOrganizationName("Microsoft")

    # Load QSS
    qss_path = os.path.join(os.path.dirname(__file__), "resources", "styles.qss")
    if os.path.exists(qss_path):
        with open(qss_path) as f:
            app.setStyleSheet(f.read())

    # Dark palette
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(26, 26, 46))
    p.setColor(QPalette.ColorRole.WindowText, QColor(200, 200, 220))
    p.setColor(QPalette.ColorRole.Base, QColor(20, 20, 40))
    p.setColor(QPalette.ColorRole.Text, QColor(200, 200, 220))
    p.setColor(QPalette.ColorRole.Highlight, QColor(68, 68, 170))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(p)

    # Tesseract
    if config.TESSERACT_PATH:
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH

    # Init components
    ocr = OCREngine(config.TESSERACT_PATH)
    ai = AIEngine(config)
    window = StealthWindow(config)

    # Pipeline: OCR detected new question → AI → display
    def handle_new_question(text):
        logger.info(f"[MAIN] Question detected ({len(text)} chars): {text[:80]}...")
        window.show_answer_streaming("Thinking...")
        for token in ai.ask(text):
            window.append_answer_token(token)
            app.processEvents()
        QTimer.singleShot(config.ANSWER_DISPLAY_SECONDS * 1000, window.clear_answer)

    ocr.text_captured.connect(handle_new_question)
    ocr.start_auto_capture(config.CAPTURE_INTERVAL_MS)
    window.show()

    # Hotkeys
    try:
        import keyboard  # type: ignore[import]
        keyboard.add_hotkey(config.TOGGLE_HOTKEY, window.toggle_visibility)
        keyboard.add_hotkey(config.MANUAL_CAPTURE_HOTKEY, lambda: (
            handle_new_question(ocr.capture_and_ocr())
        ))
        logger.info(f"[MAIN] Hotkeys: toggle={config.TOGGLE_HOTKEY}, capture={config.MANUAL_CAPTURE_HOTKEY}")
    except Exception as e:
        logger.warning(f"[MAIN] Hotkey registration failed: {e}")

    print("\n" + "=" * 55)
    print("  CoCubes Assistant v2 - RUNNING")
    print(f"  Toggle window:  {config.TOGGLE_HOTKEY}")
    print(f"  Manual capture: {config.MANUAL_CAPTURE_HOTKEY}")
    print("  Auto-captures every 2.5s (reads top-to-bottom)")
    print("=" * 55 + "\n")

    try:
        exit_code = app.exec()
    except KeyboardInterrupt:
        exit_code = 0

    ocr.stop_auto_capture()
    try:
        import keyboard  # type: ignore[import]
        keyboard.unhook_all()
    except:
        pass
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
