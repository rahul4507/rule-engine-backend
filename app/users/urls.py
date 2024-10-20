from django.urls import path

from .views.employee import EmployeeAPIView, EmployeeDetailAPIView
from .views.health import HealthCheckAPIView
from .views.user import UserLoginAPIView, LogoutAPIView, UserRegisterAPIView
from .views.rules import RuleAPIView
from .views.rules import RuleDetailView, RuleListView

app_name = "users"

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path('rules/', RuleAPIView.as_view()),
    path('rules/<int:pk>/', RuleDetailView.as_view()),
    path('rules/list/', RuleListView.as_view()),
    path('employees/', EmployeeAPIView.as_view()),
    path('employees/<int:pk>/', EmployeeAPIView.as_view()),
    path('employees/detail/<int:pk>/', EmployeeDetailAPIView.as_view()),
]