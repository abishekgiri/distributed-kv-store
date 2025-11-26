from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import uvicorn

from .config import get_config
from .state import kv_state
from .replication import init_replicator, get_replicator

config = get_config()
app = FastAPI(title=f"Distributed KV Node {config['NODE_ID']}")


class PutRequest(BaseModel):
    key: str
    value: str


class ReplicateRequest(BaseModel):
    key: str
    value: str


@app.on_event("startup")
async def startup_event():
    print(f"[{config['NODE_ID']}] starting as {config['ROLE']}, peers={config['PEERS']}")
    init_replicator(config["PEERS"])


@app.get("/health")
async def health():
    """Simple health check endpoint."""
    store, version = kv_state.dump_all()
    return {
        "status": "ok",
        "node": config["NODE_ID"],
        "role": config["ROLE"],
        "version": version,
        "key_count": len(store),
    }


@app.get("/meta")
async def meta():
    """Metadata about this node (for debugging / paper screenshots)."""
    return {
        "node": config["NODE_ID"],
        "role": config["ROLE"],
        "port": config["PORT"],
        "peers": config["PEERS"],
    }


@app.get("/get/{key}")
async def get_key(key: str):
    value, version = kv_state.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value, "version": version, "node": config["NODE_ID"]}


@app.post("/put")
async def put_key(req: PutRequest):
    if config["ROLE"] != "leader":
        raise HTTPException(status_code=403, detail="Writes only allowed on leader")

    version = kv_state.put(req.key, req.value)
    print(f"[{config['NODE_ID']}] PUT {req.key}={req.value}, version={version}")

    replicator = get_replicator()
    if replicator is not None:
        asyncio.create_task(replicator.replicate_put(req.key, req.value))

    return {"status": "ok", "version": version}


@app.post("/replicate")
async def replicate_put(req: ReplicateRequest):
    version = kv_state.put(req.key, req.value)
    print(f"[{config['NODE_ID']}] REPLICATED {req.key}={req.value}, version={version}")
    return {"status": "replicated", "version": version}


@app.get("/debug/state")
async def debug_state():
    store, version = kv_state.dump_all()
    return {
        "node": config["NODE_ID"],
        "role": config["ROLE"],
        "version": version,
        "store": store,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config["PORT"])
