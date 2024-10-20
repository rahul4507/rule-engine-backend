from django.db import models


class DepartmentType(models.IntegerChoices):
    SALES = 1, 'Sales'
    MARKETING = 2, 'Marketing'
    HR = 3, 'Human Resources'
    IT = 4, 'Information Technology'
    FINANCE = 5, 'Finance'
