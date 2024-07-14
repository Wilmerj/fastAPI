from jwt import encode, decode

secret_key_encryption: str = "my_secret_key"

def create_token(data: dict):
    token: str = encode(payload=data, key=secret_key_encryption, algorithm="HS256")
    return token;

def validate_token(token: str) -> dict:
    try:
        data: dict = decode(token, key=secret_key_encryption, algorithms=["HS256"])
        return data
    except:
        return None