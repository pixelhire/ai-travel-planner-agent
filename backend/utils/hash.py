import hashlib
import json

def generate_hash(data: dict) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()