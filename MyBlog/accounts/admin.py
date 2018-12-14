from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['username','email','email_confirmed']

admin.site.register(User,UserAdmin)
