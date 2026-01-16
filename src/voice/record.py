import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path

def record_audio(
    filename: str = "input.wav",
    duration: int = 5,
    sample_rate: int = 16000
):
    print(f"🎙 Recording for {duration} seconds...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    write(filename, sample_rate, audio)
    print(f"✅ Saved audio to {filename}")

    return Path(filename)
