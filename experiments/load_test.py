import argparse
import asyncio
import random
import time
import httpx
import csv
import os
from datetime import datetime


LEADER = "http://localhost:8000"
NODES = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
]


async def do_put(client, key, value):
    try:
        resp = await client.post(f"{LEADER}/put", json={"key": key, "value": value})
        return resp.status_code == 200
    except Exception:
        return False


async def do_get(client, key):
    try:
        node = random.choice(NODES)
        resp = await client.get(f"{node}/get/{key}")
        return resp.status_code == 200
    except Exception:
        return False


async def worker(mode, total_requests, success_counter, failure_counter, concurrency):
    async with httpx.AsyncClient(timeout=2.0) as client:
        local_latencies = []

        for _ in range(total_requests):
            key = f"key{random.randint(1, 1000)}"
            value = f"value{random.randint(1, 1000)}"

            start = time.time()

            if mode == "write-heavy":
                ok = await do_put(client, key, value)
            elif mode == "read-heavy":
                await do_put(client, key, value)  # warm-up
                ok = await do_get(client, key)
            else:
                # mixed
                if random.random() < 0.5:
                    ok = await do_put(client, key, value)
                else:
                    ok = await do_get(client, key)

            end = time.time()

            local_latencies.append((end - start) * 1000)  # ms

            if ok:
                success_counter.append(1)
            else:
                failure_counter.append(1)

        return local_latencies


async def run_load(mode, requests, concurrency):
    per_worker = requests // concurrency

    success_counter = []
    failure_counter = []

    tasks = [
        worker(mode, per_worker, success_counter, failure_counter, concurrency)
        for _ in range(concurrency)
    ]

    start = time.time()
    results = await asyncio.gather(*tasks)
    end = time.time()

    latencies = [lat for lst in results for lat in lst]

    if not latencies:
        print("No requests completed.")
        return

    latencies.sort()
    avg = sum(latencies) / len(latencies)
    p50 = latencies[int(0.50 * len(latencies))]
    p95 = latencies[int(0.95 * len(latencies))]
    p99 = latencies[int(0.99 * len(latencies))]

    total_time = end - start
    throughput = len(latencies) / total_time

    success = len(success_counter)
    failures = len(failure_counter)

    # === SAVE TO CSV ===
    os.makedirs("results", exist_ok=True)
    csv_path = "results/load_results.csv"
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp",
                "mode",
                "total_requests",
                "success",
                "failures",
                "concurrency",
                "avg_latency_ms",
                "p50_ms",
                "p95_ms",
                "p99_ms",
                "throughput_rps",
            ])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            mode,
            len(latencies),
            success,
            failures,
            concurrency,
            f"{avg:.2f}",
            f"{p50:.2f}",
            f"{p95:.2f}",
            f"{p99:.2f}",
            f"{throughput:.2f}",
        ])

    # === PRINT SUMMARY ===
    print("\n=== Load Test Summary ===")
    print(f"Mode:          {mode}")
    print(f"Total requests:{len(latencies)}")
    print(f"Success:       {success}")
    print(f"Failures:      {failures}")
    print(f"Total time:    {total_time:.2f} s")
    print(f"Throughput:    {throughput:.2f} req/s")
    print(f"Avg latency:   {avg:.2f} ms")
    print(f"P50 latency:   {p50:.2f} ms")
    print(f"P95 latency:   {p95:.2f} ms")
    print(f"P99 latency:   {p99:.2f} ms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mixed", "read-heavy", "write-heavy"], required=True)
    parser.add_argument("--requests", type=int, default=500)
    parser.add_argument("--concurrency", type=int, default=20)
    args = parser.parse_args()

    asyncio.run(run_load(args.mode, args.requests, args.concurrency))
