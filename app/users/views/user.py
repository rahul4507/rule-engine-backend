from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings
from ..models import User
from rest_framework.permissions import IsAuthenticated
import jwt


class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            token = user.token
            user.jwt_token = token
            user.update_last_active()
            return Response({"token": token}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.jwt_token = None
            user.save()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "Invalid authentication. Could not decode token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "username": user.username,
            "name": user.name,
            "last_active": user.last_active
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Extract user data from the request
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')

        # Check if email and username are unique
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User.objects.create(
            email=email,
            username=username,
            name=name,
            password=make_password(password)  # Hash the password
        )

        user.save()

        # Optionally return a JWT token upon successful registration
        token = user.token

        return Response({
            "message": "User registered successfully",
            "token": token
        }, status=status.HTTP_201_CREATED)
