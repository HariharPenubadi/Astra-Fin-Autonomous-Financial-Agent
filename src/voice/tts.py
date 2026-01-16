import subprocess
from pathlib import Path

VOICE_MODEL = "models/tts/en_US-lessac-medium.onnx"

def speak(text: str):
    output = Path("output.wav")
    cmd = [
        "piper",
        "--model", VOICE_MODEL,
        "--output_file", str(output)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    proc.stdin.write(text.encode())
    proc.stdin.close()
    proc.wait()

    subprocess.run(["afplay", str(output)])
