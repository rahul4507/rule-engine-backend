from django.urls import path

from users.views.health import HealthCheckAPIView

from users.views.user import LoginView, LogoutView, UserAPIView

app_name = "users"

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view()),
    path('register/', UserAPIView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", UserAPIView.as_view()),
]