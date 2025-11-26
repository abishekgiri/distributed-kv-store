# 6. Results

This section evaluates the distributed key–value store under three workload patterns: mixed, read-heavy, and write-heavy. All experiments were executed using the `load_test.py` harness, which generates concurrent HTTP clients and records per-request latency statistics and aggregate throughput. Each run is appended to `results/load_results.csv`, and figures are generated using `plot_results.py` and saved in `paper/figures/`.

## 6.1 Throughput Across Workload Modes

Figure 1 (**throughput_by_mode.png**) reports the average throughput for mixed, read-heavy, and write-heavy workloads. The mixed workload achieves the highest throughput (≈ 400–410 requests per second), while read-heavy and write-heavy workloads achieve roughly half of that. This reflects the cost of sustaining either very frequent reads (contention and locking) or very frequent writes (replication overhead) on a single leader.

## 6.2 Latency vs Concurrency (Mixed Workload)

Figure 2 (**latency_vs_concurrency_mixed.png**) shows how latency evolves as we increase the number of concurrent clients for the mixed workload. The average latency increases from roughly 10 ms at 5 clients to over 70 ms at 50 clients. The p95 latency grows more quickly, exceeding 400 ms at the highest concurrency level. This behavior is consistent with queueing effects at the leader and the cost of replicating each write to two followers.

## 6.3 Read-Heavy Workload

Figure 3 (**latency_vs_concurrency_read-heavy.png**) summarizes the latency of the read-heavy workload at 40 concurrent clients. Even though reads may be served from any node, the average latency is still on the order of hundreds of milliseconds, and p95 latency is higher. This suggests that under heavy concurrency, contention on the in-memory state and background replication still impact end-to-end response time, even for read-dominated workloads.

## 6.4 Write-Heavy Workload

Figure 4 (**latency_vs_concurrency_write-heavy.png**) shows the latency for the write-heavy workload at 20 concurrent clients. Average latency is higher than in the mixed case, and p95 latency is over 300 ms. This is expected, since each write must be processed by the leader and then forwarded to all followers, effectively multiplying the work for each client request.

## 6.5 Summary

Overall, the prototype achieves several hundred requests per second with sub-100 ms average latency at moderate concurrency levels. As concurrency increases, average latency rises smoothly while p95 latency grows more sharply, highlighting the impact of replication and single-leader bottlenecks on tail performance. These trends are typical of leader–follower replicated systems and provide a solid baseline for exploring optimizations such as batching, sharding, or leader election in future work.
