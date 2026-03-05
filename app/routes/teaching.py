from flask import Blueprint, request, jsonify

from app.services.asr_service import ASRService
from app.services.teaching_service import TeachingService
from app.services.tts_service import TTSService

teaching_bp = Blueprint("teaching", __name__)

asr_service = ASRService()
teacher = TeachingService()
tts = TTSService()


@teaching_bp.route("/ask", methods=["POST"])
def ask_question():

    if "file" not in request.files:
        return jsonify({"error": "audio file missing"}), 400

    audio = request.files["file"]

    filepath = "uploads/question.wav"
    audio.save(filepath)

    # ASR
    asr_result = asr_service.transcribe_audio(filepath)

    topic = asr_result["transcript"]

    # GPT explanation
    explanation = teacher.generate_explanation(topic)

    # TTS speech
    speech_file = tts.generate_speech(explanation)

    return jsonify({
        "question": topic,
        "explanation": explanation,
        "speech_file": speech_file
    })
@teaching_bp.route("/text", methods=["POST"])
def text_teaching():

    data = request.get_json()

    question = data["question"]

    explanation = teacher.generate_explanation(question)

    speech_file = tts.generate_speech(explanation)

    return jsonify({
        "question": question,
        "explanation": explanation,
        "speech_file": speech_file
    })