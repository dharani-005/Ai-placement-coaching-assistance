from flask import Blueprint, request, jsonify
import os
import uuid

from app.services.asr_service import ASRService
from app.services.teaching_service import TeachingService
from app.services.tts_service import TTSService

teaching_bp = Blueprint("teaching", __name__)

asr_service = ASRService()
teacher = TeachingService()
tts = TTSService()

UPLOAD_FOLDER = "uploads"


@teaching_bp.route("/ask", methods=["POST"])
def ask_question():

    if "file" not in request.files:
        return jsonify({"error": "audio file missing"}), 400

    audio = request.files["file"]

    # Generate unique filename
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    audio.save(filepath)

    # Speech to text
    asr_result = asr_service.transcribe_audio(filepath)

    topic = asr_result["transcript"]

    # Generate explanation using GPT
    explanation = teacher.generate_explanation(topic)

    # Convert explanation to speech
    speech_file = tts.generate_speech(explanation)

    return jsonify({
        "question": topic,
        "explanation": explanation,
        "speech_file": speech_file
    })


@teaching_bp.route("/text", methods=["POST"])
def text_teaching():

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "question missing"}), 400

    question = data["question"]

    # Generate explanation
    explanation = teacher.generate_explanation(question)

    # Generate speech
    speech_file = tts.generate_speech(explanation)

    return jsonify({
        "question": question,
        "explanation": explanation,
        "speech_file": speech_file
    })