from django.utils import timezone
from django.db import models
from django.utils.datetime_safe import datetime


class Rule(models.Model):
    name = models.CharField(max_length=255)
    rule_string = models.TextField(unique=True, null=True, blank=True)
    ast = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class meta:
        app_label = "users"
        db_table = "rule"

    def __str__(self):
        return self.name
