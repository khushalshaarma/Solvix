import logging
from PyQt6.QtCore import Qt, QTimer, QPoint  # type: ignore[import]
from PyQt6.QtGui import QFont, QTextCursor  # type: ignore[import]
from PyQt6.QtWidgets import (  # type: ignore[import]
    QApplication, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, 
    QWidget, QTextBrowser, QFrame
)

logger = logging.getLogger(__name__)


class AnswerDisplay(QTextBrowser):
    """Rich text answer display with color-coding and formatting.
    Supports HTML for answer highlighting (green for correct, yellow for options, etc.)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenExternalLinks(False)
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMinimumHeight(100)
        self.setMinimumWidth(280)
        self.setMaximumWidth(600)
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.document().setDefaultFont(font)
        self.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(20, 20, 45, 230);
                color: #E0E0FF;
                border: 1px solid rgba(100, 100, 200, 60);
                border-radius: 8px;
                padding: 12px 16px;
                selection-background-color: #4444AA;
            }
            QScrollBar:vertical {
                background: rgba(26, 26, 46, 100);
                width: 6px;
                margin: 0;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(100, 100, 200, 120);
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

    def set_answer(self, text: str):
        """Set answer with automatic HTML formatting."""
        html = self._format_answer(text)
        self.setHtml(html)
        self.verticalScrollBar().setValue(0)

    def append_stream(self, text: str):
        """Append streaming text while preserving HTML formatting."""
        # Convert plain text tokens to safe HTML and append
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe = safe.replace("\n", "<br>")
        
        cursor = self.textCursor()
        # move to document end using QTextCursor API
        try:
            cursor.movePosition(QTextCursor.MoveOperation.End)
        except Exception:
            # fallback to legacy enum name
            try:
                cursor.movePosition(QTextCursor.End)
            except Exception:
                # last resort: set position to end of document
                cursor.setPosition(len(self.toPlainText()))
        
        # Color code based on content
        if "Answer:" in safe:
            safe = f'<span style="color:#00FF88;font-weight:bold;">{safe}</span>'
        elif "Explanation:" in safe:
            safe = f'<span style="color:#88CCFF;">{safe}</span>'
        elif "UNCERTAIN" in safe:
            safe = f'<span style="color:#FF8888;">{safe}</span>'
        elif safe.startswith("[ERROR"):
            safe = f'<span style="color:#FF4444;">{safe}</span>'
        
        cursor.insertHtml(safe)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def show_thinking(self):
        self.setHtml('<div style="color:#8888AA; font-style:italic;">⏳ Analyzing question...</div>')

    def clear_answer(self):
        self.clear()

    @staticmethod
    def _format_answer(text: str) -> str:
        """Convert plain answer to color-coded HTML."""
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe = safe.replace("\n", "<br>")
        
        # Style the answer beautifully
        lines = safe.split("<br>")
        html_lines = []
        for line in lines:
            if line.startswith("Answer:"):
                html_lines.append(f'<div style="color:#00FF88; font-weight:bold; font-size:13px; margin-top:6px;">{line}</div>')
            elif line.startswith("Explanation:"):
                html_lines.append(f'<div style="color:#88CCFF; font-size:11px; margin-top:4px;">{line}</div>')
            elif line.startswith("[ERROR"):
                html_lines.append(f'<div style="color:#FF4444;">{line}</div>')
            elif line.startswith("UNCERTAIN"):
                html_lines.append(f'<div style="color:#FFAA44; font-weight:bold;">{line}</div>')
            elif line.strip():
                html_lines.append(f'<div style="color:#CCCCDD;">{line}</div>')
            else:
                html_lines.append("<br>")
        
        return f"""
        <html>
        <body style="font-family:'Consolas','Segoe UI',monospace; font-size:11px;">
            <div style="background:rgba(20,20,45,0); padding:4px;">
                {''.join(html_lines)}
            </div>
        </body>
        </html>
        """


class StealthWindow(QMainWindow):
    """Frameless stealth window with rich text answer display."""

    def __init__(self, config):
        super().__init__()
        self.cfg = config
        self.status = {}
        self._visible = True
        self._drag_pos = QPoint()

        # Window flags for maximum stealth
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, True)
        self.setWindowOpacity(config.WINDOW_OPACITY)
        self.setObjectName("stealthWindow")

        self._build_ui()
        self._position()

        logger.info("[UI] StealthWindow ready")

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        outer = QVBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Title bar (draggable) ──
        title = QWidget()
        title.setFixedHeight(28)
        title.setObjectName("titleBar")
        title.setStyleSheet("""
            QWidget#titleBar {
                background: rgba(26,26,46,200);
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid rgba(100,100,200,50);
            }
        """)
        tlo = QHBoxLayout()
        tlo.setContentsMargins(10, 2, 10, 2)
        icon = QLabel("⬥")
        icon.setStyleSheet("color:#8888FF; font-size:14px;")
        lbl = QLabel("Exam Assistant")
        lbl.setStyleSheet("color:#8888FF; font-size:11px; font-weight:bold;")
        self.status_icon = QLabel("●")
        self.status_icon.setStyleSheet("color:#44CC44; font-size:10px;")
        tlo.addWidget(icon)
        tlo.addWidget(lbl)
        tlo.addStretch()
        tlo.addWidget(self.status_icon)
        title.setLayout(tlo)

        # Make title draggable
        title.mousePressEvent = self._drag_start
        title.mouseMoveEvent = self._drag_move

        # ── Answer display ──
        self.display = AnswerDisplay()
        self.display.setMinimumHeight(120)

        # ── Status bar ──
        self.status_label = QLabel("🛡 Stealth Active")
        self.status_label.setFixedHeight(18)
        self.status_label.setStyleSheet("color:#666688; font-size:9px; padding:2px 10px;")

        outer.addWidget(title)
        outer.addWidget(self.display, 1)
        outer.addWidget(self.status_label)
        central.setLayout(outer)
        self.setCentralWidget(central)

        # Default size
        self.resize(self.cfg.WINDOW_WIDTH, self.cfg.WINDOW_HEIGHT)

    def _drag_start(self, event):
        self._drag_pos = event.globalPosition().toPoint()
        event.accept()

    def _drag_move(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def _position(self):
        screen = QApplication.primaryScreen()
        if screen:
            g = screen.availableGeometry()
            self.move(g.right() - self.width() - 10, g.bottom() - self.height() - 45)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(200, self._apply_stealth)

    def _apply_stealth(self):
        try:
            from utils.anti_forensic import apply_all_stealth
            self.status = apply_all_stealth(self)
            if self.status.get("anti_capture"):
                self.status_label.setText("🛡 Protected | Anti-capture active")
                self.status_icon.setStyleSheet("color:#44CC44; font-size:10px;")
            else:
                self.status_label.setText("⚠ Partial protection")
                self.status_icon.setStyleSheet("color:#FFAA44; font-size:10px;")
        except Exception as e:
            logger.warning(f"[UI] Stealth apply failed: {e}")

    # ── Public API ──
    def show_answer_streaming(self, text="Thinking..."):
        self.display.show_thinking()
        self.show()
        self.raise_()
        self.activateWindow()

    def append_answer_token(self, token: str):
        self.display.append_stream(token)

    def set_answer(self, text: str):
        self.display.set_answer(text)

    def clear_answer(self):
        self.display.clear_answer()

    def toggle_visibility(self):
        if self._visible:
            self.hide()
            self._visible = False
        else:
            self.show()
            self.raise_()
            self._visible = True
