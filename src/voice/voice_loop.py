from src.voice.record import record_audio
from src.voice.stt import transcribe
from src.voice.tts import speak
from src.graph.astra_graph import build_graph

def run_voice():
    graph = build_graph()

    print("🎤 Speak to ASTRA (Ctrl+C to stop)")

    while True:
        audio_path = record_audio(duration=5)

        query = transcribe(str(audio_path))
        print("You:", query)
        if not query or len(query.split()) < 2:
            print("⚠️ Ignoring noise / silence")
            continue

        result = graph.invoke({
            "query": query,
            "disable_web": True
        })

        answer = result.get("review") or result.get("answer")

        print("ASTRA:", answer)
        speak(answer)
