from faster_whisper import WhisperModel
import time
import os

# 🔧 FIX: Disable symlink warnings BEFORE any imports
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

class ASRService:
    def __init__(self):
        """
        Initialize Faster-Whisper model (loads ONCE at server start).
        Fixed for Windows symlink errors + optimized for entry-level CPU.
        """
        cpu_threads = os.cpu_count() or 4
        
        self.model = WhisperModel(
            "distil-large-v3",       # Same accuracy as large-v2, 40% smaller/faster
            device="cpu",
            compute_type="int8",     # 2-3x speedup
            cpu_threads=cpu_threads  # Use all CPU cores
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

        # Run transcription WITH NOISE REDUCTION + optimizations
        segments, info = self.model.transcribe(
            filepath,
            language="en",
            beam_size=5,
            word_timestamps=True,
            vad_filter=True,                    # 🔥 NOISE REDUCTION
            vad_parameters=dict(
                min_silence_duration_ms=500,
                threshold=0.5
            ),
            condition_on_previous_text=False
        )

        transcript = ""
        word_segments = []

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
