# Generate an overall JSON summary of buildtime-latency-size sets for easy Pareto analysis
import json
import csv
import os

results = []

def process_csv(filename):
    rows = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            rows.append(row)

    return rows

for file in os.listdir("./benchmark_results"):
    results.extend(process_csv("./benchmark_results/" + file))

indexes = {}
for row in results:
    name, variant, latency, size, build_time, searcher, dataset = row
    if name not in indexes:
        indexes[name] = {}
    if dataset not in indexes[name]:
        indexes[name][dataset] = []
    indexes[name][dataset].append({
        "latency": float(latency),
        "size": int(size),
        "build_time": int(float(build_time))
    })

with open("./_data/all_results.json", "w") as f:
    json.dump(indexes, f)