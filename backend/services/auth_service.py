from core.security import create_token

def login(username: str, password: str):
    # Replace with DB validation later
    if username == "admin" and password == "admin":
        return create_token({"user": username})

    return None
