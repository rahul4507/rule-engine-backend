from django.db import models
from ..utils.choices import DepartmentType


class Employee(models.Model):
    age = models.IntegerField()
    department = models.CharField(
        max_length=50,
        choices=DepartmentType.choices,
        null=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.IntegerField()

    class meta:
        app_label = "users"
        db_table = "employee"

    def __str__(self):
        return f"{self.department} Employee - Age: {self.age}"