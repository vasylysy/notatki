import argon2, re
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad


def encrypt_password(
        password, t=16, m=2 ** 17, p=4, hash_len=32, salt_len=16
):
    argon2hasher = argon2.PasswordHasher(
        time_cost=t,
        memory_cost=m,
        parallelism=p,
        hash_len=hash_len,
        salt_len=salt_len,
    )
    hash = argon2hasher.hash(password)
    return hash


def verify_password(
        hash, password, t=16, m=2 ** 17, p=4, hash_len=32, salt_len=16
):
    argon2hasher = argon2.PasswordHasher(
        time_cost=t,
        memory_cost=m,
        parallelism=p,
        hash_len=hash_len,
        salt_len=salt_len,
    )
    try:
        is_valid = argon2hasher.verify(hash, password)
    except:
        return False
    else:
        return is_valid


def strength_password(password):
    strength = 0
    if len(password) < 8:
        return strength
    if re.search(r'[A-Z]', password):
        strength += 1
    if re.search(r'[a-z]', password):
        strength += 1
    if re.search(r'[0-9]', password):
        strength += 1
    if re.search(r"\W", password):
        strength += 1
    return strength


def encrypt_note(decrypted, salt):
    key = PBKDF2(bytes('password','utf-8'), bytes(salt,'utf-8'))
    data=decrypted.encode('utf-8')
    data_padded = pad(data, 16)
    aes = AES.new(key, AES.MODE_ECB)
    encrypted = aes.encrypt(data_padded)
    return encrypted

def more_encrypt_note(decrypted, salt):
    key = PBKDF2(bytes('password', 'utf-8'), bytes(salt, 'utf-8'))
    if len(salt) < 16:
        salt = salt * len(salt)
    iv = bytes(salt[:16], 'utf-8')
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    data_padded = pad(decrypted.encode('utf-8'), 16)
    encrypted = aes.encrypt(data_padded)
    return encrypted

def decrypt_note(encrypted, salt):
    key = PBKDF2(bytes('password','utf-8'), bytes(salt,'utf-8'))
    data_padded = encrypted
    aes = AES.new(key, AES.MODE_ECB)
    decrypted = unpad(aes.decrypt(data_padded), 16).decode('utf-8')
    return decrypted

def more_decrypt_note(encrypted, salt):
    key = PBKDF2(bytes('password', 'utf-8'), bytes(salt, 'utf-8'))
    if len(salt) < 16:
        salt = salt*len(salt)
    iv = bytes(salt[:16], 'utf-8')
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    data_padded = encrypted
    decrypted = unpad(aes.decrypt(data_padded), 16).decode('utf-8')
    return decrypted