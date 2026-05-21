import logging
import os
from typing import Generator

try:
    from PyQt6.QtCore import QObject, pyqtSignal  # type: ignore
except ImportError:
    class QObject:
        def __init__(self, *args, **kwargs):
            pass

    class _Signal:
        def emit(self, *args, **kwargs):
            pass

    def pyqtSignal(*args, **kwargs):
        return _Signal()

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai  # type: ignore[import]
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False; genai = None

try:
    import ollama  # type: ignore[import]
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False; ollama = None

class AIEngine(QObject):
    token_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.cfg = config
        self.backend = config.AI_BACKEND.lower()
        self.history = []
        self._model = None
        self._init_backend()

    def _init_backend(self):
        if self.backend == "gemini":
            self._init_gemini()
        elif self.backend == "ollama":
            self._init_ollama()

    def _init_gemini(self):
        if not HAS_GEMINI:
            logger.error("[AI] Install: pip install google-generativeai")
            return
        key = self.cfg.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        if not key:
            logger.error("[AI] No Gemini API key. Set in config.py or env GEMINI_API_KEY")
            logger.error("[AI] Get free key: https://aistudio.google.com/apikey")
            return
        genai.configure(api_key=key)
        self._model = genai.GenerativeModel(
            self.cfg.GEMINI_MODEL,
            system_instruction=self.cfg.SYSTEM_PROMPT
        )
        logger.info(f"[AI] Gemini {self.cfg.GEMINI_MODEL} ready")

    def _init_ollama(self):
        if not HAS_OLLAMA:
            logger.error("[AI] Install: pip install ollama")
            return
        try:
            ollama.list()
            logger.info(f"[AI] Ollama connected at {self.cfg.OLLAMA_BASE_URL}")
        except Exception as e:
            logger.error(f"[AI] Ollama connection failed: {e}")

    def ask(self, question: str) -> Generator[str, None, None]:
        if self.backend == "gemini" and self._model:
            yield from self._ask_gemini(question)
        elif self.backend == "ollama":
            yield from self._ask_ollama(question)
        else:
            yield "[ERROR] No AI backend available"

    def _ask_gemini(self, question: str) -> Generator[str, None, None]:
        try:
            chat = self._model.start_chat()
            resp = chat.send_message(f"Question:\n{question}\n\nAnswer:", stream=True)
            full = ""
            for chunk in resp:
                if chunk.text:
                    full += chunk.text
                    yield chunk.text
            self.history += [{"role":"user","content":question},{"role":"assistant","content":full}]
        except Exception as e:
            yield f"\n[ERROR: {e}]"
            self.error_occurred.emit(str(e))

    def _ask_ollama(self, question: str) -> Generator[str, None, None]:
        try:
            msgs = [{"role":"system","content":self.cfg.SYSTEM_PROMPT}]
            for e in self.history[-4:]:
                msgs.append({"role":e["role"],"content":e["content"]})
            msgs.append({"role":"user","content":question})
            stream = ollama.chat(model=self.cfg.OLLAMA_MODEL, messages=msgs, stream=True)
            full = ""
            for chunk in stream:
                tok = chunk.get("message",{}).get("content","")
                if tok:
                    full += tok; yield tok
            self.history += [{"role":"user","content":question},{"role":"assistant","content":full}]
        except Exception as e:
            yield f"\n[ERROR: {e}]"
            self.error_occurred.emit(str(e))

    def clear_history(self):
        self.history.clear()
