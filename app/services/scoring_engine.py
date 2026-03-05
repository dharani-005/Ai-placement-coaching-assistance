class ScoringEngine:

    def calculate_score(self, analytics, evaluation):

        relevance = evaluation["relevance"]
        keyword = evaluation["keyword_coverage"]
        structure = evaluation["structure_clarity"]

        fluency = analytics["fluency_score"]
        filler_count = analytics["filler_count"]
        wpm = analytics["wpm"]

        # WPM Balance
        if 110 <= wpm <= 150:
            wpm_score = 10
        elif 90 <= wpm < 110 or 150 < wpm <= 170:
            wpm_score = 7
        else:
            wpm_score = 4

        # Filler Penalty
        filler_penalty = min(filler_count * 1, 10)

        final_score = (
            relevance
            + keyword
            + structure
            + fluency
            + wpm_score
            - filler_penalty
        )

        final_score = max(0, min(final_score, 100))

        return {
            "final_score": final_score,
            "breakdown": {
                "relevance": relevance,
                "keyword": keyword,
                "structure": structure,
                "fluency": fluency,
                "wpm_score": wpm_score,
                "filler_penalty": filler_penalty
            }
        }