from django.db import models

class DepartmentType(models.TextChoices):
    SALES = 'Sales', 'Sales'
    MARKETING = 'Marketing', 'Marketing'
    HR = 'Human Resources', 'Human Resources'
    IT = 'Information Technology', 'Information Technology'
    FINANCE = 'Finance', 'Finance'
