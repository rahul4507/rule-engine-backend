from django.contrib import admin

from .models.rule import Rule
from .models.user import User

# Register your models here.
admin.site.register(User)
admin.site.register(Rule)