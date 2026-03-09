import bcrypt


def hash_password(raw_password: str) -> str:
    return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()


def matches_password(raw_password: str, stored_password: str) -> bool:
    """BCrypt 해시 또는 평문 비밀번호 모두 지원 (기존 DB 호환)"""
    if stored_password.startswith("$2"):
        return bcrypt.checkpw(raw_password.encode(), stored_password.encode())
    return raw_password == stored_password
