import secrets
import string


def generate_username() -> str:
    alphabet = string.ascii_letters
    username = "".join(secrets.choice(alphabet) for i in range(8))
    return username


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphabet) for i in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password

