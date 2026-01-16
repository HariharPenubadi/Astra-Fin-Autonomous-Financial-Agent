import whisper
import numpy as np
import soundfile as sf

model = whisper.load_model("base")

SILENCE_THRESHOLD = 0.01  # energy threshold

def is_silent(audio_path: str) -> bool:
    data, _ = sf.read(audio_path)
    return np.abs(data).mean() < SILENCE_THRESHOLD


def transcribe(audio_path: str) -> str:
    if is_silent(audio_path):
        return ""

    result = model.transcribe(
        audio_path,
        temperature=0.0,
        no_speech_threshold=0.6,
        logprob_threshold=-0.5,
    )

    text = result["text"].strip()

    if len(text.split()) < 3:
        return ""

    return text
