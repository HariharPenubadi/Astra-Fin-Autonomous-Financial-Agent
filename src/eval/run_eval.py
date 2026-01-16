import json
from src.eval.metrics import evaluate

with open("data/eval/finance_eval.json") as f:
    dataset = json.load(f)

results = evaluate(dataset)

accuracy = sum(r["grounded"] for r in results) / len(results)

print("Grounded Accuracy:", round(accuracy * 100, 2), "%")
print("Average Latency:",
      round(sum(r["latency"] for r in results) / len(results), 2), "sec")
