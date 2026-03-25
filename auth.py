from datetime import UTC, timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from config import settings
import jwt

password_hash= PasswordHash.recommended()
Oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/users/token")

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hash_password)

def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime(UTC).now() + expires_delta
    else:
        expire = datetime(UTC).now + timedelta(
            minutes=settings.access_token_expiry_minutes,
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key.get_secret_value(),
            algorithm=settings.algorithm,
        )
        return encoded_jwt
    
def verify_access(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ['exp', 'sub']},
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")