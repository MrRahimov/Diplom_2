import time
import random
import string

BASE_URL = "https://stellarburgers.education-services.ru/api"


def uniq_email(prefix: str = "autotest") -> str:
    return f"{prefix}_{int(time.time() * 1000)}@example.com"


def rand_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def default_user() -> dict:
    return {
        "email": uniq_email(),
        "password": rand_password(),
        "name": "Auto Tester",
    }
