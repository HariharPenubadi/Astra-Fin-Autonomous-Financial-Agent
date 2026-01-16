from src.graph.astra_graph import build_graph
from src.voice.voice_loop import run_voice
from src.memory.short_term import add_turn

def run():
    mode = input("Mode (text/voice): ").strip().lower()

    if mode == "voice":
        run_voice()
        return

    graph = build_graph()
    while True:
        query = input("\nUser > ")
        if query.lower() in ["exit", "quit"]:
            break

        result = graph.invoke({"query": query})

        if "answer" in result and result["answer"]:
            print(f"\nASTRA > {result['answer']}")
            add_turn(query, result["answer"])
        else:
            print("\nASTRA > I couldn’t generate a confident answer yet.")
            add_turn(query, result["answer"])


if __name__ == "__main__":
    run()
