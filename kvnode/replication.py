from typing import List, Optional
import httpx


class Replicator:
    def __init__(self, peers: List[str]):
        self.peers = peers
        print(f"[Replicator] configured with peers = {self.peers}")

    async def replicate_put(self, key: str, value: str):
        if not self.peers:
            print("[Replicator] no peers configured, skipping replication")
            return

        async with httpx.AsyncClient(timeout=2.0) as client:
            for base in self.peers:
                url = f"{base}/replicate"
                try:
                    resp = await client.post(url, json={"key": key, "value": value})
                    print(f"[Replicator] sent to {url}, status={resp.status_code}")
                except Exception as e:
                    print(f"[Replicator] ERROR sending to {url}: {e}")


_replicator: Optional[Replicator] = None


def init_replicator(peers: List[str]):
    global _replicator
    _replicator = Replicator(peers)


def get_replicator() -> Optional[Replicator]:
    return _replicator
