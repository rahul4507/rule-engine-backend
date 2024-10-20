import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(max_length=50, db_index=True, unique=True)
    last_active = models.DateField(null=True, blank=True)
    jwt_token = models.CharField(max_length=200, null=True)
    is_staff = models.BooleanField(default=False)  # <- admin user, not super user
    is_superuser = models.BooleanField(default=False)  # <- super user

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        app_label = "users"
        db_table = "user"
        unique_together = ("email", "username")
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "email",
                    "username",
                ],
                name="unique email username",
            )
        ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

