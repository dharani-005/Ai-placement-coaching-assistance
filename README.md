# 🎙️ VoiceHire AI – Intelligent Voice-Based Interview & Teaching Assistant

VoiceHire AI is a full-stack AI-powered system that simulates real-time technical interviews and teaching assistance using voice input. It combines speech recognition, natural language understanding, AI evaluation, and text-to-speech to deliver a human-like interactive experience.

---

## 🚀 Features

### 🎯 Interview Mode

* 🎤 Voice-based interaction
* 🤖 AI-generated **natural interview questions**
* 🧠 Context-aware question generation (OOP, DBMS, HR, etc.)
* 📊 Answer evaluation using AI
* 💬 Human-like feedback (not robotic scoring)
* 🔊 Voice feedback using TTS
* 🔁 Avoids repeated questions using SQLite

---

### 📘 Teaching Mode

* 🎤 Ask questions via voice or text
* 📖 AI explains concepts clearly
* 🔊 Audio explanation output
* 🧠 Context-aware explanations (definition, example, concept)

---

## 🧠 Tech Stack

### Backend

* Python (Flask)
* Faster-Whisper (ASR)
* OpenAI API (GPT-4.1 nano)
* SQLite (question tracking)
* Text-to-Speech (TTS)

### Frontend

* HTML, CSS, JavaScript
* MediaRecorder API (audio recording)

---

## ⚙️ System Architecture

```
User Voice
   ↓
Faster Whisper (Speech-to-Text)
   ↓
Intent Detection (Interview / Teaching)
   ↓
AI Processing (GPT)
   ↓
Evaluation / Explanation
   ↓
Text-to-Speech
   ↓
Voice Output
```

---

## 📂 Project Structure

```
voicehire/
│
├── app/
│   ├── routes/
│   │   ├── interview.py
│   │   ├── teaching.py
│   │
│   ├── services/
│   │   ├── asr_service.py
│   │   ├── evaluation_service.py
│   │   ├── interview_agent_service.py
│   │   ├── speech_analytics.py
│   │   ├── scoring_engine.py
│   │   ├── teaching_service.py
│   │   ├── tts_service.py
│   │   ├── interview_db_service.py
│
├── uploads/
├── ui/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│
├── main.py
├── config.py
├── requirements.txt
```

---

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd voicehire
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install FFmpeg (Required for ASR)

Download:
👉 https://www.gyan.dev/ffmpeg/builds/

Add `ffmpeg/bin` to system PATH.

---

### 5. Set Environment Variables

Create `.env` file:

```
OPENAI_API_KEY=your_api_key
```

---

### 6. Run Application

```bash
python main.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## ⚡ Performance Optimization

* Faster-Whisper (medium + int8) for fast CPU inference
* GPT-4.1 nano for low-latency AI responses
* Model loads once at startup
* SQLite for lightweight storage

---

## 🧪 Example Usage

### Interview Mode

```
User: Ask me OOP questions
AI: Can you explain what polymorphism is?
User: (answers)
AI: Provides human-like feedback
```

---

### Teaching Mode

```
User: Explain abstraction
AI: Gives explanation + audio output
```

---

## 🔐 Error Handling

* Handles API failures gracefully
* Prevents server crashes
* Validates audio input
* Avoids duplicate questions

---

## 📌 Future Improvements

* Adaptive questioning based on user performance
* Resume-based interview personalization
* Multi-language support
* Real-time streaming ASR
* Cloud deployment (Docker + GPU)

---

## 👨‍💻 Author

**Dharanidharan R**

---

## ⭐ Acknowledgment

* OpenAI API
* Faster-Whisper
* Flask Framework

---

## 📄 License

This project is for academic and educational use.
