import secrets


def generate_password(length: int = 8) -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(length))
