from datetime import datetime, timezone

from jose import JWTError, jwt

from app.config import settings

ALGORITHM = "HS256"


def create_access_token(user_id: str, roles: list[str]) -> str:
    return _create_token(user_id, roles, settings.JWT_ACCESS_EXPIRATION)


def create_refresh_token(user_id: str) -> str:
    return _create_token(user_id, None, settings.JWT_REFRESH_EXPIRATION)


def _create_token(user_id: str, roles: list[str] | None, expiration_ms: int) -> str:
    now = datetime.now(timezone.utc)
    exp = datetime.fromtimestamp(now.timestamp() + expiration_ms / 1000, tz=timezone.utc)
    payload: dict = {"sub": user_id, "iat": now, "exp": exp}
    if roles is not None:
        payload["roles"] = roles
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def get_user_id(token: str) -> str:
    claims = _parse_claims(token)
    return claims["sub"]


def get_roles(token: str) -> list[str]:
    claims = _parse_claims(token)
    return claims.get("roles", [])


def validate_token(token: str) -> bool:
    try:
        _parse_claims(token)
        return True
    except (JWTError, Exception):
        return False


def _parse_claims(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
