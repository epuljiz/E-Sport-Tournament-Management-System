import bcrypt

def hash_password(plain: str) -> str:
    """Hashira lozinku s bcrypt algoritmom. Vraća string spreman za bazu."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    """Provjerava podudara li se plain lozinka s hashom iz baze."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())
