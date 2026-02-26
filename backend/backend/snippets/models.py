from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Potrzebne do powiązania Snippetu z nowym Użytkownikiem

class Uzytkownik(AbstractUser):
    # Pola: username, password, first_name (imię), last_name (nazwisko), email
    numer_indeksu = models.CharField(max_length=5, blank=True, null=True, verbose_name="Numer indeksu")
    grupa_dziekanska = models.CharField(max_length=20, blank=True, null=True, verbose_name="Kod Grupy")

    is_student = models.BooleanField(default=True, verbose_name="Czy to student?")
    is_teacher = models.BooleanField(default=False, verbose_name="Czy to prowadzący?")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Snippet(models.Model):
    LANGUAGES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', "Java"),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGES, default='python')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
