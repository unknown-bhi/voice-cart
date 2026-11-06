from cryptography.fernet import Fernet
from app.core.config import settings

if not settings.FERNET_KEY:
    raise ValueError('FERNET_KEY is not set in environment variables.')

cipher_suite = Fernet(settings.FERNET_KEY.encode())

def encrypt_data(data : str):

    return cipher_suite.encrypt(data.encode())

def decrypt_data(encrypted_data:bytes):

    return cipher_suite.decrypt(encrypted_data).decode()

