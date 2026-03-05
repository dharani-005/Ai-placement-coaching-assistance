import random
from app.services.question_bank import QUESTION_BANK
from app.services.interview_db_service import get_asked_questions, store_question


class InterviewAgent:

    def detect_topic(self, text):

        text = text.lower()

        if "oop" in text or "object" in text:
            return "oop"

        if "dbms" in text:
            return "dbms"

        if "self intro" in text or "introduce" in text:
            return "hr"

        return "oop"


    def generate_question(self, text):

        topic = self.detect_topic(text)

        questions = QUESTION_BANK[topic]

        asked = get_asked_questions()

        available = [q for q in questions if q not in asked]

        if not available:
            available = questions

        question = random.choice(available)

        store_question(question)

        return question