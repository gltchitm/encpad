import hmac
import string
import hashlib

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from secrets import token_hex
from json import dumps, loads
from store import store

def pad(string):
    remainder = len(string) % AES.block_size
    padding_needed = AES.block_size - remainder
    return string + " " * padding_needed
def hex_hmac(private_key, plain_text):
    return hmac.new(
        private_key,
        bytes(plain_text, "utf-8"),
        hashlib.sha256
    ).hexdigest()

def hash_pw(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha512",
        bytes(password, "utf-8"),
        bytes(salt, "utf-8"),
        500_000,
        32
    )
def encrypt(plain_text, password):
    salt = token_hex(8)
    iv = token_hex(8)
    padded_text = pad(plain_text)
    private_key = hash_pw(password, salt)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded_text)
    return b64encode(
        bytes(
            dumps({
                "cipher_text": b64encode(encrypted).decode("utf-8"),
                "hmac": hex_hmac(private_key, plain_text),
                "salt": salt,
                "iv": iv
            }),
            "utf-8"
        ) 
    ).decode("utf-8")
def decrypt(encrypted_str, password):
    encrypted = loads(b64decode(encrypted_str))
    cipher_text = b64decode(encrypted["cipher_text"])
    private_key = hash_pw(password, encrypted["salt"])
    cipher = AES.new(private_key, AES.MODE_CBC, encrypted["iv"])
    try:
        decrypted = cipher.decrypt(cipher_text).rstrip().decode("utf-8")
    except UnicodeDecodeError:
        return
    if not hmac.compare_digest(hex_hmac(private_key, decrypted), encrypted["hmac"]):
        return
    return decrypted
