import secrets

def generate_secret_key(length=32):
    """Generate a random secret key."""
    return secrets.token_hex(length)

SECRET_KEY = generate_secret_key()

DB_HOST = '172.16.20.244'
DB_NAME = 'appusers'
DB_USER = 'Gowtham'
DB_PASSWORD = 'Gc176720!'
DB_ROOT_PASSWORD = 'Gc176720@'
