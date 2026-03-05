import whisper
import time
import os
from config import Config

class ASRService:

    def __init__(self):
        # Load model once (important for performance)
        self.model = whisper.load_model("large")

    def transcribe_audio(self, filepath):
        """
        Transcribes audio and returns:
        - transcript text
        - word timestamps
        - duration
        - stt latency
        """

        start_time = time.time()

        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            raise ValueError("Audio file is empty or not saved correctly")
        
        result = self.model.transcribe(
        filepath,
        language="en",
        task="transcribe",
        word_timestamps=True,
        beam_size=5,
        best_of=5,
        temperature=0,
        fp16=False
)

        end_time = time.time()

        transcript = result["text"].strip()

        # Extract word-level timestamps
        word_segments = []
        for segment in result["segments"]:
            if "words" in segment:
                for word_info in segment["words"]:
                    word_segments.append({
                        "word": word_info["word"],
                        "start": word_info["start"],
                        "end": word_info["end"]
                    })

        duration = word_segments[-1]["end"] if word_segments else 0
        stt_latency = round(end_time - start_time, 3)

        return {
            "transcript": transcript,
            "timestamps": word_segments,
            "duration": duration,
            "stt_latency": stt_latency
        }