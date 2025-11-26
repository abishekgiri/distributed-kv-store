import os


def get_config():
    peers_env = os.getenv("PEERS", "")
    peers = [p.strip() for p in peers_env.split(",") if p.strip()]

    return {
        "NODE_ID": os.getenv("NODE_ID", "node1"),
        "ROLE": os.getenv("ROLE", "leader"),  # "leader" or "follower"
        "PORT": int(os.getenv("PORT", "8000")),
        "PEERS": peers,  # list of base URLs like ["http://node2:8001", "http://node3:8002"]
    }
