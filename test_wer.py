from app.services.wer_service import WERService

wer_service = WERService()

reference = "I am a third year computer science student"
transcript = "I am third year computer science student"

wer = wer_service.calculate_wer(reference, transcript)

print("WER:", wer)