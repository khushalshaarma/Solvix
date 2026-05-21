from PyQt6.QtCore import Qt  # type: ignore[import]
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget  # type: ignore[import]

class AnswerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._label = QLabel("Ready...")
        self._label.setWordWrap(True)
        self._label.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self._label.setObjectName("answerLabel")
        lo = QVBoxLayout()
        lo.setContentsMargins(0,0,0,0)
        lo.addWidget(self._label)
        self.setLayout(lo)
        self.setMinimumWidth(280)

    def set_answer(self, text: str):
        self._label.setText(text); self.adjustSize()

    def append_text(self, text: str):
        cur = self._label.text()
        self._label.setText(text if cur in ("Ready...","") else cur+text)
        self.adjustSize()

    def clear(self):
        self._label.setText(""); self.adjustSize()

    def show_thinking(self):
        self._label.setText("Thinking..."); self.adjustSize()
