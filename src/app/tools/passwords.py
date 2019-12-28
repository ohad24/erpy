import binascii
from hashlib import pbkdf2_hmac
from setup import app
# from uuid import uuid4
import os


def hash_password(password):
    """ returns hexadecimal string of pbkdf2 password hash """
    if not isinstance(password, str):
        raise TypeError('password must be str')
    salt = app.secret_key  # MUST NOT CHANGE !!!
    hash_bytes = pbkdf2_hmac('sha256', password.encode(), salt.encode(), 4096)
    return binascii.hexlify(hash_bytes).decode()
