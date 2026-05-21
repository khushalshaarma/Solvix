Solvix

An AI-powered desktop study assistant built with Python and PyQt6 for practice exams, OCR-based question extraction, and instant AI explanations using Google Gemini or Ollama.

Features
Real-time OCR question detection
Floating desktop assistant window
AI-generated answers and explanations
Gemini API support
Ollama local LLM support
Dark modern UI
Hotkey controls
Automatic screen capture
Streaming AI responses
Lightweight PyQt6 interface
Tech Stack
Python 3.11+
PyQt6
Tesseract OCR
OpenCV
MSS Screen Capture
Google Gemini API
Ollama
Pillow
Folder Structure
prep_pilot_ai/
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
Installation
1. Clone Repository
git clone https://github.com/yourusername/Solvix.git
cd Solvix
2. Create Virtual Environment
python -m venv venv
3. Activate Environment
Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
4. Install Requirements
pip install -r requirements.txt
Install Tesseract OCR

Download and install:

Tesseract OCR GitHub

Default Windows path:

C:\Program Files\Tesseract-OCR\tesseract.exe
Gemini API Setup

Get a free Gemini API key from:

Google AI Studio

Add your API key inside config.py:

GEMINI_API_KEY = "your_api_key_here"
Running the Project
python main.py
Hotkeys
Hotkey	Action
Ctrl + `	Toggle assistant window
Ctrl + Shift + C	Manual OCR capture
OCR Workflow
Capture screen region
Extract text using Tesseract OCR
Send text to Gemini/Ollama
Display AI-generated response
Auto-clear after timeout
Example Use Cases
Practice exams
Coding interview prep
MCQ solving
Educational assistance
Study sessions
Local AI experimentation
Requirements
PyQt6>=6.5.0
requests>=2.31.0
google-generativeai>=0.7.0
ollama>=0.4.0
pytesseract>=0.3.10
pillow>=10.0.0
mss>=9.0.0
keyboard>=0.13.5
opencv-python>=4.8.0
Screenshots

Add screenshots here:

resources/screenshots/
Future Improvements
Multi-monitor support
Voice assistant mode
Better OCR preprocessing
Chat history
Local vector memory
Whisper speech-to-text
GPU acceleration
Disclaimer

This project is intended for educational purposes, accessibility support, and practice environments only. Users are responsible for complying with the policies and rules of any examination platform or institution.

License

MIT License
