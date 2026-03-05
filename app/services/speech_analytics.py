import re

class SpeechAnalytics:

    FILLER_WORDS = [
        "um", "uh", "like", "actually", "basically",
        "you know", "i mean", "sort of", "kind of"
    ]

    def analyze(self, transcript, timestamps, duration):

        words = transcript.split()
        total_words = len(words)

        # ---- WPM ----
        if duration > 0:
            wpm = round((total_words / duration) * 60, 2)
        else:
            wpm = 0

        # ---- Filler Detection ----
        filler_count = 0
        transcript_lower = transcript.lower()

        for filler in self.FILLER_WORDS:
            filler_count += transcript_lower.count(filler)

        # ---- Pause Detection ----
        pause_count = 0
        previous_end = None

        for word in timestamps:
            if previous_end is not None:
                gap = word["start"] - previous_end
                if gap > 2:
                    pause_count += 1
            previous_end = word["end"]

        # ---- Repetition Detection ----
        repetition_count = 0
        word_list = [w.lower() for w in words]

        for i in range(len(word_list) - 1):
            if word_list[i] == word_list[i+1]:
                repetition_count += 1

        # ---- Fluency Score ----
        fluency_score = max(0, 15 - pause_count - repetition_count)

        return {
            "total_words": total_words,
            "wpm": wpm,
            "filler_count": filler_count,
            "pause_count": pause_count,
            "repetition_count": repetition_count,
            "fluency_score": fluency_score
        }