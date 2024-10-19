from django.urls import path

from users.views.health import HealthCheckAPIView
from users.views.user import LoginView, LogoutView, UserAPIView
from users.views.rules import RuleCreateAPIView
from users.views.rules import RuleDetailView, RuleListView

app_name = "users"

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view()),
    path('register/', UserAPIView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", UserAPIView.as_view()),
    path('rules/', RuleCreateAPIView.as_view()),
    path('rules/<int:pk>/', RuleDetailView.as_view()),
    path('rules/list/', RuleListView.as_view()),
]