from django.db import models
from ..utils.choices import DepartmentType


class Employee(models.Model):
    age = models.IntegerField()
    department = models.IntegerField(
        choices=DepartmentType.choices,
        null=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.IntegerField()

    def __str__(self):
        return f"{self.department} Employee - Age: {self.age}"