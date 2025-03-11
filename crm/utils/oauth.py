import jwt
import random

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.conf import settings


class FakeUser:
    """
    A fake user object for authentication purposes in the second app.
    """

    def __init__(self, core_user_uuid, username):
        self.id = random.randint(1, 1000)
        self.username = username
        self.core_user_uuid = core_user_uuid
        self.is_authenticated = True  # Force authentication
        self.is_superuser = False

    def __str__(self):
        return self.username


class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication class that validates and authenticates users
    based on the token generated from the generate_access_tokens function.
    """

    def authenticate(self, request):
        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split('Bearer ')[1]

        try:
            # Decode the token
            payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=['HS256'])

            # Extract user details
            core_user_uuid = payload.get("core_user_uuid")
            username = payload.get("username", '')

            if not core_user_uuid:
                raise AuthenticationFailed("Invalid token payload")

            # Create a fake user object
            fake_user = FakeUser(core_user_uuid, username)
            return fake_user, None

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed("Invalid token")

    def authenticate_header(self, request):
        return 'Bearer'
