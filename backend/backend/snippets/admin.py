from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Snippet, Uzytkownik

# Register your models here.
admin.site.register(Uzytkownik, UserAdmin)
admin.site.register(Snippet)
