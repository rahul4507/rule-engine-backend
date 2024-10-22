from rest_framework import serializers
from ..models import Employee, DepartmentType


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.ChoiceField(choices=DepartmentType.choices)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'age', 'department', 'salary', 'experience']
