from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

from argon2.low_level import hash_secret_raw, Type as Argon2Type

def encrypt(data, password):
    salt = get_random_bytes(32)
    key = hash_secret_raw(
        password,
        salt,
        time_cost=4,
        memory_cost=88064,
        parallelism=3,
        hash_len=32,
        type=Argon2Type.ID
    )
    nonce = get_random_bytes(24)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return salt + nonce + ciphertext + tag

def decrypt(encrypted, password):
    salt = encrypted[0:32]
    nonce = encrypted[32:32 + 24]
    ciphertext = encrypted[32 + 24:len(encrypted) - 16]
    tag = encrypted[len(encrypted) - 16:]

    key = hash_secret_raw(
        password,
        salt,
        time_cost=4,
        memory_cost=88064,
        parallelism=3,
        hash_len=32,
        type=Argon2Type.ID
    )

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)

    return cipher.decrypt_and_verify(ciphertext, tag)
