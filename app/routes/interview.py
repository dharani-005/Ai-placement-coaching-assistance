from flask import Blueprint, request, jsonify
import os
import time

from app.services.asr_service import ASRService
from app.services.speech_analytics import SpeechAnalytics
from app.services.evaluation_service import EvaluationService
from app.services.scoring_engine import ScoringEngine
from app.services.interview_agent_service import InterviewAgent
from app.services.tts_service import TTSService

agent = InterviewAgent()
tts = TTSService()
interview_bp = Blueprint("interview", __name__)
current_question = None
asr_service = ASRService()
analytics = SpeechAnalytics()
evaluator = EvaluationService()
scoring = ScoringEngine()

UPLOAD_FOLDER = "uploads"


@interview_bp.route("/upload", methods=["POST"])
def upload_audio():

    pipeline_start = time.time()   # moved inside

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    if "question" not in request.form:
        return jsonify({"error": "Question missing"}), 400

    question = request.form["question"]

    audio = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(filepath)

    # Step 1 — ASR
    asr_result = asr_service.transcribe_audio(filepath)

    # Step 2 — Speech Analytics
    analytics_result = analytics.analyze(
        asr_result["transcript"],
        asr_result["timestamps"],
        asr_result["duration"]
    )

    # Step 3 — GPT Evaluation
    evaluation_start = time.time()

    evaluation = evaluator.evaluate_answer(
        question,
        asr_result["transcript"]
    )

    evaluation_end = time.time()
    evaluation_latency = round(evaluation_end - evaluation_start, 3)

    # Step 4 — Scoring
    score = scoring.calculate_score(
        analytics_result,
        evaluation
    )

    pipeline_end = time.time()
    total_latency = round(pipeline_end - pipeline_start, 3)

    return jsonify({
        "question": question,
        "transcript": asr_result["transcript"],
        "analytics": analytics_result,
        "evaluation": evaluation,
        "score": score,
        "latency": {
            "stt_latency": asr_result["stt_latency"],
            "evaluation_latency": evaluation_latency,
            "total_latency": total_latency
        }
    })
@interview_bp.route("/question", methods=["POST"])
def ask_question():

    global current_question

    if "file" not in request.files:
        return jsonify({"error": "No audio"}), 400

    audio = request.files["file"]

    filepath = os.path.join("uploads", audio.filename)
    audio.save(filepath)

    asr_result = asr_service.transcribe_audio(filepath)

    transcript = asr_result["transcript"]

    question = agent.generate_question(transcript)
    current_question = question

    speech = tts.generate_speech(question)

    return jsonify({
        "transcript": transcript,
        "question": question,
        "audio": speech
    })

@interview_bp.route("/text", methods=["POST"])
def ask_text_question():

    global current_question

    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data["prompt"]
    question = agent.generate_question(prompt)
    current_question = question

    speech = tts.generate_speech(question)

    return jsonify({
        "prompt": prompt,
        "question": question,
        "audio": speech
    })

@interview_bp.route("/answer", methods=["POST"])
def evaluate_answer():

    global current_question

    if "file" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio = request.files["file"]
    filepath = os.path.join("uploads", audio.filename)
    audio.save(filepath)

    # Speech to text
    asr_result = asr_service.transcribe_audio(filepath)
    transcript = asr_result["transcript"]

    # Speech analytics
    analytics_result = analytics.analyze(
        transcript,
        asr_result["timestamps"],
        asr_result["duration"]
    )

    # GPT evaluation
    evaluation = evaluator.evaluate_answer(
        current_question,
        transcript
    )

    # scoring
    score = scoring.calculate_score(
        analytics_result,
        evaluation
    )

    feedback_text = evaluator.generate_feedback(
        current_question,
        transcript,
        score,
        evaluation
    )
    speech = tts.generate_speech(feedback_text)

    return jsonify({
        "transcript": transcript,
        "score": score,
        "feedback": feedback_text,
        "audio": speech
    })