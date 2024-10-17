from django.urls import path

from users.views.health import HealthCheckAPIView

app_name = "users"

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view()),
]