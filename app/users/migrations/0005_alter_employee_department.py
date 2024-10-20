# Generated by Django 4.2 on 2024-10-20 07:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_employee_rule_created_date_rule_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="department",
            field=models.CharField(
                choices=[
                    ("Sales", "Sales"),
                    ("Marketing", "Marketing"),
                    ("Human Resources", "Human Resources"),
                    ("Information Technology", "Information Technology"),
                    ("Finance", "Finance"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
