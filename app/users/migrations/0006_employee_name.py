# Generated by Django 4.2 on 2024-10-22 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_employee_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]