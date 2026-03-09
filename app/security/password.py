from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def matches_password(raw_password: str, stored_password: str) -> bool:
    """BCrypt 해시 또는 평문 비밀번호 모두 지원 (기존 DB 호환)"""
    if stored_password.startswith("$2"):
        return pwd_context.verify(raw_password, stored_password)
    return raw_password == stored_password
