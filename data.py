from api.models.models import User
from auth.auth_util import get_password_hash

user_db = {
    "user1": {
        "username": "user1",
        "email": "email1@example.com",
        "password": get_password_hash("password1")
    },
    "user2": {
        "username": "user2",
        "email": "email2@example.com",
        "password": get_password_hash("password2")
    },
}