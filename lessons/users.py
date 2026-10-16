import hashlib
import hmac
import json
import os
from pathlib import Path

USERS_FILE = Path(__file__).parent.parent / "users.json"

def _load() -> dict:
    return json.loads(USERS_FILE.read_text()) if USERS_FILE.exists() else {}

def _hash(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000).hex()

def add_user(username: str, password: str, role: str) -> None:
    users = _load()
    salt = os.urandom(16)
    users[username] = {
        "salt": salt.hex(),
        "hash": _hash(password,salt),
        "role": role
    }
    USERS_FILE.write_text(json.dumps(users, indent=2))

def verify_login(username: str, password: str):
    """ Return the user's role if the password is right, otherwise None"""
    user = _load().get(username)
    if user is None:
        return None
    candidate = _hash(password, bytes.fromhex(user["salt"]))
    return user["role"] if hmac.compare_digest(candidate, user["hash"]) else None

if __name__ =="__main__":
    add_user("alice", "alice123", "viewer")
    add_user("bob", "bob123", "packing")
    add_user("carol", "carol123", "admin")
    print(verify_login("alice", "alice123"))
    print(verify_login("alice","wrong"))
    print(verify_login("nobody","x"))

