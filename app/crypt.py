import argon2, re


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
