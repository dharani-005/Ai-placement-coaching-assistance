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
current_topic = None
current_difficulty_index = 0
difficulty_levels = ["basic", "intermediate", "advanced"]
has_asked_topic = False
asr_service = ASRService()
analytics = SpeechAnalytics()
evaluator = EvaluationService()
scoring = ScoringEngine()

UPLOAD_FOLDER = "uploads"


def should_reset_topic(text):
    if not text:
        return False
    lowered = text.lower().strip()
    return (
        "change topic" in lowered
        or "change the topic" in lowered
        or "switch topic" in lowered
        or "switch the topic" in lowered
        or "chage topic" in lowered
        or "chage the topic" in lowered
    )


@interview_bp.route("/start", methods=["GET"])
def start_interview():
    global current_topic
    global current_difficulty_index
    global has_asked_topic
    global current_question

    current_topic = None
    current_question = None
    current_difficulty_index = 0
    has_asked_topic = True

    question = "What topic should I ask you about?"
    speech = tts.generate_speech(question)
    return jsonify({
        "question": question,
        "audio": speech
    })


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
    global current_topic
    global current_difficulty_index
    global has_asked_topic

    if "file" not in request.files:
        return jsonify({"error": "No audio"}), 400

    audio = request.files["file"]

    filepath = os.path.join("uploads", audio.filename)
    audio.save(filepath)

    asr_result = asr_service.transcribe_audio(filepath)
    try:
        os.remove(filepath)
    except OSError:
        pass

    transcript = asr_result["transcript"]

    if should_reset_topic(transcript):
        current_topic = None
        current_difficulty_index = 0
        has_asked_topic = False
        question = "What topic should I ask you about?"
        has_asked_topic = True
        speech = tts.generate_speech(question)
        return jsonify({
            "transcript": transcript,
            "question": question,
            "audio": speech
        })

    if not has_asked_topic:
        question = "What topic should I ask you about?"
        has_asked_topic = True
        speech = tts.generate_speech(question)
        return jsonify({
            "transcript": transcript,
            "question": question,
            "audio": speech
        })

    if current_topic is None:
        current_topic = transcript

    difficulty = difficulty_levels[current_difficulty_index]
    question = agent.generate_question(current_topic, difficulty)
    current_question = question

    speech = tts.generate_speech(question)

    return jsonify({
        "transcript": transcript,
        "question": question,
        "difficulty": difficulty,
        "audio": speech
    })


@interview_bp.route("/text", methods=["POST"])
def ask_text_question():

    global current_question
    global current_topic
    global current_difficulty_index
    global has_asked_topic

    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data["prompt"]

    if should_reset_topic(prompt):
        current_topic = None
        current_difficulty_index = 0
        has_asked_topic = False
        question = "What topic should I ask you about?"
        has_asked_topic = True
        speech = tts.generate_speech(question)
        return jsonify({
            "prompt": prompt,
            "question": question,
            "audio": speech
        })

    if not has_asked_topic:
        question = "What topic should I ask you about?"
        has_asked_topic = True
        speech = tts.generate_speech(question)
        return jsonify({
            "prompt": prompt,
            "question": question,
            "audio": speech
        })

    if current_topic is None:
        current_topic = prompt

    difficulty = difficulty_levels[current_difficulty_index]
    question = agent.generate_question(current_topic, difficulty)
    current_question = question

    speech = tts.generate_speech(question)

    return jsonify({
        "prompt": prompt,
        "question": question,
        "difficulty": difficulty,
        "audio": speech
    })

@interview_bp.route("/answer", methods=["POST"])
def evaluate_answer():

    global current_question
    global current_topic
    global current_difficulty_index
    global has_asked_topic

    transcript = None

    if "file" in request.files:
        audio = request.files["file"]
        filepath = os.path.join("uploads", audio.filename)
        audio.save(filepath)

        # Speech to text
        asr_result = asr_service.transcribe_audio(filepath)
        try:
            os.remove(filepath)
        except OSError:
            pass
        transcript = asr_result["transcript"]
        analytics_result = analytics.analyze(
            transcript,
            asr_result["timestamps"],
            asr_result["duration"]
        )
    elif request.is_json:
        data = request.get_json()
        if not data or "answer" not in data:
            return jsonify({"error": "No answer provided"}), 400
        transcript = data["answer"]
        analytics_result = analytics.analyze(transcript, [], 0)
    else:
        return jsonify({"error": "No answer provided"}), 400

    if current_question is None:
        return jsonify({"error": "No active question to evaluate"}), 400

    if should_reset_topic(transcript):
        current_question = None
        current_topic = None
        has_asked_topic = False
        current_difficulty_index = 0
        question = "What topic should I ask you about?"
        has_asked_topic = True
        speech = tts.generate_speech(question)
        return jsonify({
            "transcript": transcript,
            "question": question,
            "feedback": "Topic reset. Please tell me which topic you'd like to practice next.",
            "audio": speech
        })

    evaluation = evaluator.evaluate_answer(
        current_question,
        transcript
    )

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
    feedback_audio = tts.generate_speech(feedback_text)

    if current_difficulty_index < len(difficulty_levels) - 1:
        current_difficulty_index += 1

    next_question = agent.generate_question(
        current_topic,
        difficulty_levels[current_difficulty_index]
    )
    current_question = next_question

    return jsonify({
        "transcript": transcript,
        "score": score,
        "feedback": feedback_text,
        "audio": feedback_audio,
        "next_question": next_question
    })