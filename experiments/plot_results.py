import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict


CSV_PATH = "results/load_results.csv"


def load_csv():
    if not os.path.isfile(CSV_PATH):
        raise FileNotFoundError("CSV file not found. Run load_test.py at least once.")

    rows = []
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["concurrency"] = int(r["concurrency"])
            r["throughput_rps"] = float(r["throughput_rps"])
            r["avg_latency_ms"] = float(r["avg_latency_ms"])
            r["p95_ms"] = float(r["p95_ms"])
            rows.append(r)
    return rows


def plot_latency_vs_concurrency(rows, mode="mixed"):
    xs = []
    avg = []
    p95 = []

    for r in rows:
        if r["mode"] == mode:
            xs.append(r["concurrency"])
            avg.append(r["avg_latency_ms"])
            p95.append(r["p95_ms"])

    if not xs:
        print(f"No data for mode {mode}")
        return

    pairs = sorted(zip(xs, avg, p95), key=lambda p: p[0])
    xs = [p[0] for p in pairs]
    avg = [p[1] for p in pairs]
    p95 = [p[2] for p in pairs]

    plt.figure()
    plt.plot(xs, avg, marker="o", label="Average Latency")
    plt.plot(xs, p95, marker="x", label="P95 Latency")
    plt.title(f"Latency vs Concurrency ({mode})")
    plt.xlabel("Concurrency")
    plt.ylabel("Latency (ms)")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"results/latency_vs_concurrency_{mode}.png")
    plt.close()
    print(f"Saved latency_vs_concurrency_{mode}.png")


def plot_throughput_by_mode(rows):
    modes = defaultdict(list)

    for r in rows:
        modes[r["mode"]].append(float(r["throughput_rps"]))

    names = list(modes.keys())
    vals = [sum(v) / len(v) for v in modes.values()]

    plt.figure()
    plt.bar(names, vals)
    plt.title("Average Throughput by Workload Mode")
    plt.xlabel("Mode")
    plt.ylabel("Throughput (req/s)")
    plt.savefig("results/throughput_by_mode.png")
    plt.close()
    print("Saved throughput_by_mode.png")


if __name__ == "__main__":
    rows = load_csv()
    plot_latency_vs_concurrency(rows, "mixed")
    plot_latency_vs_concurrency(rows, "read-heavy")
    plot_latency_vs_concurrency(rows, "write-heavy")
    plot_throughput_by_mode(rows)
