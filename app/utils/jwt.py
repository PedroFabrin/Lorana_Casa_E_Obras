import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", 60))


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None
