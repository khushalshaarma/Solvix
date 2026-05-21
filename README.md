<div align="center">

# ⚡ Solvix

### AI-Powered Desktop Study Assistant

<img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge">
<img src="https://img.shields.io/badge/OCR-Tesseract-red?style=for-the-badge">
<img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge">

<br>

An intelligent desktop assistant built using **Python + PyQt6** that combines  
OCR, AI models, and a modern floating UI for real-time study assistance.

</div>

---

# ✨ Features

- 🔍 Real-time OCR question detection
- 🪟 Floating desktop assistant window
- 🤖 AI-generated answers & explanations
- 🧠 Google Gemini API support
- 🦙 Ollama local LLM support
- 🌙 Modern dark UI
- ⌨️ Hotkey controls
- 📸 Automatic screen capture
- ⚡ Streaming AI responses
- 🪶 Lightweight PyQt6 interface

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core Language |
| PyQt6 | Desktop UI |
| Tesseract OCR | Text Extraction |
| OpenCV | Image Processing |
| MSS | Fast Screen Capture |
| Gemini API | AI Responses |
| Ollama | Local AI Models |
| Pillow | Image Handling |

---

# 📂 Project Structure

```bash
Solvix/
├── main.py
├── config.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── ai_engine.py
│   └── ocr_engine.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── ui/
│   ├── __init__.py
│   ├── floating_window.py
│   └── answer_widget.py
└── resources/
    └── styles.qss
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/Solvix.git
cd Solvix
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔠 Install Tesseract OCR

Download and install:

👉 https://github.com/tesseract-ocr/tesseract

Default Windows path:

```python
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

# 🔑 Gemini API Setup

Get your free Gemini API key:

👉 https://aistudio.google.com/

Add API key inside `config.py`

```python
GEMINI_API_KEY = "your_api_key_here"
```

---

# ▶️ Running the Project

```bash
python main.py
```

---

# ⌨️ Hotkeys

| Hotkey | Action |
|---|---|
| `Ctrl + \`` | Toggle Window |
| `Ctrl + Shift + C` | Manual OCR Capture |

---

# 🔄 OCR Workflow

```text
Capture Screen
      ↓
Extract Text via OCR
      ↓
Send to Gemini/Ollama
      ↓
Generate AI Response
      ↓
Display Answer in Floating UI
```

---

# 💡 Example Use Cases

- 📚 Practice Exams
- 💻 Coding Interview Preparation
- 📝 MCQ Solving
- 🎓 Educational Assistance
- 🧪 AI Experimentation
- 🖥️ Desktop Productivity

---

# 📦 Requirements

```txt
PyQt6>=6.5.0
requests>=2.31.0
google-generativeai>=0.7.0
ollama>=0.4.0
pytesseract>=0.3.10
pillow>=10.0.0
mss>=9.0.0
keyboard>=0.13.5
opencv-python>=4.8.0
```

---

# 📸 Screenshots

Add screenshots inside:

```bash
resources/screenshots/
```

Example:

```md
![UI Preview](resources/screenshots/ui.png)
```

---

# 🚀 Future Improvements

- 🖥️ Multi-monitor support
- 🎤 Voice assistant mode
- 🧠 Better OCR preprocessing
- 💬 Chat history
- 📚 Local vector memory
- 🎧 Whisper speech-to-text
- ⚡ GPU acceleration

---

# ⚠️ Disclaimer

This project is intended for:

- Educational purposes
- Accessibility support
- Practice environments
- AI experimentation

Users are responsible for complying with the rules and policies of any examination platform or institution.

---

# 📜 License

MIT License

---

<div align="center">

### Built with ❤️ using Python, AI & PyQt6

⭐ Star the repository if you like the project.

</div>
