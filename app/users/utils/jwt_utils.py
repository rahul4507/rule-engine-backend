import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from ..models import User

class JWTAuthenticationMiddleware(MiddlewareMixin):
    authentication_header_prefix = "Bearer"
    def process_request(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or len(auth_header) != 2:
            return None

        token = auth_header[1].decode("utf-8")
        if token:
            try:
                # Extract the token value from 'Bearer <token>'
                token = token.split(' ')[1]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                user = User.objects.get(id=user_id)
                request.user = user
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
