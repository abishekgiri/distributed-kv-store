# Distributed Key–Value Store with Leader-Based Replication
## Paper Outline

1. **Introduction**
   - Motivation: scalable, fault-tolerant storage for cloud-native microservices
   - Problem: simple, explainable replicated store for experimentation
   - Contributions:
     - Implementation of a 3-node leader–follower KV store in FastAPI
     - Async HTTP-based replication and experimental evaluation
     - Open-source style project structure suitable for teaching / research

2. **Background and Related Work**
   - Key–value stores (Redis, Dynamo-style systems, etc.)
   - Replication models: primary–backup, leader–follower, quorum reads/writes
   - Consistency vs availability trade-offs (CAP-style discussion)

3. **System Design**
   - Overall architecture: one leader, two followers
   - Data model and operations (PUT/GET, versions)
   - Replication protocol (leader fan-out on write)
   - Failure model and assumptions (no network partitions, crash-stop failures)

4. **Implementation**
   - Codebase structure (`kvnode`, `experiments`, `docker`, `paper`)
   - Node configuration via environment variables
   - In-memory state management and versioning
   - Replication module and async HTTP calls with `httpx`
   - Containerization with Docker and multi-node setup with Docker Compose

5. **Experimental Methodology**
   - Testbed: laptop spec, Docker environment
   - Workload generator (`load_test.py`) and parameters
   - Workload types: mixed, read-heavy, write-heavy
   - Metrics collected: throughput, average latency, p50, p95, p99
   - Automation: CSV logging and plotting pipeline

6. **Results**
   - Throughput by workload mode (Figure: `throughput_by_mode.png`)
   - Latency vs concurrency for mixed workloads
   - Latency behavior for read-heavy vs write-heavy workloads
   - Discussion of tail latency and replication overhead

7. **Discussion**
   - Strengths of the design (simplicity, clarity, reproducibility)
   - Limitations (single leader, in-memory only, no automatic re-election)
   - Trade-offs between read scalability and consistency

8. **Future Work**
   - Durability and persistent storage
   - Automatic leader election / Raft-style consensus
   - Sharding / partitioning for larger keyspaces
   - More advanced workload models and longer-running experiments

9. **Conclusion**
   - Summary of what was built and learned
   - How this prototype can be used for teaching or extended research

10. **References**
   - Key papers / systems you decide to cite (to be filled in later)
