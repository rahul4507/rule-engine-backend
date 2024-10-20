from rest_framework import serializers
from ..models import Employee
from ..utils.choices import DepartmentType

class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.ChoiceField(choices=DepartmentType.choices)

    class Meta:
        model = Employee
        fields = ['id', 'age', 'department', 'salary', 'experience']
