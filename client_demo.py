import asyncio
import httpx


LEADER = "http://localhost:8000"
FOLLOWERS = ["http://localhost:8001", "http://localhost:8002"]


async def demo():
    async with httpx.AsyncClient(timeout=2.0) as client:
        # 1) Check health of all nodes
        print("=== Health checks ===")
        for url in [LEADER] + FOLLOWERS:
            resp = await client.get(f"{url}/health")
            print(url, "->", resp.json())

        # 2) Write a value to the leader
        print("\n=== Writing key 'course' to leader ===")
        resp = await client.post(f"{LEADER}/put", json={"key": "course", "value": "Distributed Systems"})
        print("PUT response:", resp.json())

        # 3) Read from all nodes
        print("\n=== Reading 'course' from all nodes ===")
        for url in [LEADER] + FOLLOWERS:
            resp = await client.get(f"{url}/get/course")
            print(url, "->", resp.json())


if __name__ == "__main__":
    asyncio.run(demo())
