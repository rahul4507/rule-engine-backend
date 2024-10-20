from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.employee import  EmployeeEvaluateAPIView, EmployeeViewSet
from .views.health import HealthCheckAPIView
from .views.user import UserLoginAPIView, LogoutAPIView, UserRegisterAPIView
from .views.rules import RuleViewSet, CombineRulesAPIView

app_name = "users"
router = DefaultRouter()
router.register(r'rules', RuleViewSet, basename='rule')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('health/', HealthCheckAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('rules/combine/', CombineRulesAPIView.as_view()),
    path('employees/<int:pk>/evaluate/', EmployeeEvaluateAPIView.as_view()),
    path('', include(router.urls)),
]