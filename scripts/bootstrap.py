import secrets
import string


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_env_file():
    variables = {
        "FLASK_APP": "route_planning",
        "FLASK_ENV": "production",
        "SECRET_KEY": secrets.token_hex(32),
        "DB_NAME": "routeplanning",
        "DB_USER": "routeplanning",
        "DB_PASS": generate_password(),
        "DB_HOST": "localhost",
        "POSTGRES_DB": "route_planning_db",
        "POSTGRES_USER": "route_planning_user",
        "POSTGRES_PASSWORD": "${DB_PASS}",
        "MEMCACHED_SERVER": "memcached:11211",
        "ITEMS_PER_PAGE": "10",
        "BABEL_DEFAULT_LOCALE": "ro",
        "BABEL_DEFAULT_TIMEZONE": "UTC",
    }

    with open(".env", "w") as f:
        for key, value in variables.items():
            f.write(f"{key}={value}\n")

    print(".env file has been generated successfully.")


if __name__ == "__main__":
    generate_env_file()
