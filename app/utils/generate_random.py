import secrets
import string

def secure_random_string(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))