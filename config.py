from dataclasses import dataclass, field

@dataclass
class Config:
    AI_BACKEND: str = "gemini"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    GEMINI_API_KEY: str = "AIzaSyAOagmhViLdkmkT9eXh6bPPJMH8wVYsVWs"  # Get free from https://aistudio.google.com/apikey
    GEMINI_MODEL: str = "gemini-2.5-flash"
    TESSERACT_PATH: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    CAPTURE_INTERVAL_MS: int = 2500
    WINDOW_WIDTH: int = 320
    WINDOW_HEIGHT: int = 160
    ANSWER_DISPLAY_SECONDS: int = 5
    TOGGLE_HOTKEY: str = "ctrl+`"
    MANUAL_CAPTURE_HOTKEY: str = "ctrl+shift+c"
    ENABLE_ANTI_CAPTURE: bool = True
    ENABLE_PROCESS_HIDE: bool = True
    WINDOW_OPACITY: float = 0.85
    SYSTEM_PROMPT: str = field(default_factory=lambda: (
        "You are an expert exam assistant. The user provides an MCQ captured "
        "from an online exam.\n"
        "1. Analyze the question carefully.\n"
        "2. For coding questions, provide correct code.\n"
        "3. For technical MCQs, reason step-by-step and select the answer.\n"
        "4. For aptitude questions, show calculation and answer.\n"
        "5. Output ONLY the final answer concisely.\n"
        "6. If uncertain, say 'UNCERTAIN' and give your best guess.\n\n"
        "Format:\nAnswer: <option letter or text>\nExplanation: <brief>"
    ))

config = Config()
