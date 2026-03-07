from faster_whisper import WhisperModel
import time
import os


class ASRService:

    def __init__(self):
        """
        Initialize Faster-Whisper model.
        Model loads only once when server starts.
        """

        self.model = WhisperModel(
            "large-v2",
            device="cpu",
            compute_type="int8"
        )

    def transcribe_audio(self, filepath):
        """
        Transcribes audio and returns:
        - transcript text
        - word timestamps
        - duration
        - stt latency
        """

        start_time = time.time()

        # Validate audio file
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            raise ValueError("Audio file is empty or not saved correctly")

        # Run transcription
        segments, info = self.model.transcribe(
            filepath,
            language="en",
            beam_size=5,
            word_timestamps=True
        )

        transcript = ""
        word_segments = []

        # Extract transcript + word timestamps
        for segment in segments:

            transcript += segment.text

            if segment.words:
                for word in segment.words:
                    word_segments.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    })

        transcript = transcript.strip()

        end_time = time.time()

        duration = word_segments[-1]["end"] if word_segments else 0
        stt_latency = round(end_time - start_time, 3)

        return {
            "transcript": transcript,
            "timestamps": word_segments,
            "duration": duration,
            "stt_latency": stt_latency
        }