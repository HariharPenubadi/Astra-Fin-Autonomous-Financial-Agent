import time
from src.graph.astra_graph import build_graph

def evaluate(dataset):
    graph = build_graph()
    results = []

    for item in dataset:
        start = time.time()
        output = graph.invoke({"query": item["question"]})
        latency = time.time() - start

        context = output.get("context", "")
        grounded = bool(context and context.strip())

        results.append({
            "question": item["question"],
            "grounded": grounded,
            "latency": latency
        })

    return results
