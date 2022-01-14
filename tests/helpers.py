from main.libs import generate_token


def generate_authorization_header(user_id):
    return f"Bearer+ {generate_token(user_id)}"
