import hashlib
import base64
import bcrypt


def _pre_hash(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.b64encode(digest)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_pre_hash(password), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_pre_hash(plain_password), hashed_password.encode())
