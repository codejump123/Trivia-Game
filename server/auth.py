import hashlib
import os


ITERATIONS = 120_000
SALT_BYTES = 16


def hash_password(password, salt_hex=None):
    if salt_hex is None:
        salt = os.urandom(SALT_BYTES)
    else:
        salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return salt.hex(), digest.hex()


def verify_password(password, salt_hex, expected_hash):
    _, digest_hex = hash_password(password, salt_hex)
    return digest_hex == expected_hash
