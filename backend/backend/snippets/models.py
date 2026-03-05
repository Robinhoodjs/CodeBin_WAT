from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Potrzebne do powiązania Snippetu z nowym Użytkownikiem

class Uzytkownik(AbstractUser):
    '''
    AbstractUser posiada w sobie wbudowane pola: username, password, first_name, last_name, email
    '''
    ROLES = [
        ('student', 'Student'),
        ('profesor', 'Profesor'),
    ]
    rola = models.CharField(max_length=10, choices=ROLES, default='student')
    numer_indeksu = models.CharField(max_length=5, blank=True, null=True)
    grupa_dziekanska = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Snippet(models.Model):
    LANGUAGES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', "Java"),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGES, default='python')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Łatwe'),
        ('medium', 'Średnie'),
        ('hard', 'Trudne'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField() # Treść zadania może też być w formacie markdown ( .md)
    
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    # Limity techniczne potrzebne do sprawdzania kodu (HU 1.12)
    time_limit = models.IntegerField(default=1000, help_text="Limit czasu wykonania w milisekundach")
    memory_limit = models.IntegerField(default=256, help_text="Limit pamięci w megabajtach (MB)")
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    '''
    null - czyli zadanie wygenerowane przez AI
    on_delete=models.SET_NULL, null=True - gdy usunie się użytkownika, jego kody nie znikają, a autor zmienia się na null
    '''
    
    # Czy zadanie jest widoczne dla wszystkich, czy tylko dla twórcy/grupy (HU 1.3)
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"
    
class TestCase(models.Model):
    '''
    Django automatycznie doda pole task_id(foreign key)
    '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='test_cases')
    
    input_data = models.TextField(help_text="Dane wejściowe (np. '2 2' dla zadania o dodawaniu)")
    
    expected_output = models.TextField(help_text="Oczekiwany wynik (np. '4')")
    
    # Niektóre testy pokazujemy użytkownikowi w treści zadania, inne są ukryte (do ostatecznego sprawdzania).
    is_sample = models.BooleanField(default=False, help_text="Czy to jest test przykładowy widoczny dla użytkownika?")
    
    # Opcjonalne punkty za przejście tego konkretnego testu (przydatne do statystyk)
    points = models.IntegerField(default=0)

    def __str__(self):
        typ_testu = "Przykładowy" if self.is_sample else "Ukryty"
        return f"Test {typ_testu} do zadania: {self.task.title}"
    
class Solution(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Oczekujące na sprawdzenie'),
        ('accepted', 'Zaakceptowane (Zaliczony)'),
        ('wrong_answer', 'Błędna odpowiedź'),
        ('time_limit', 'Przekroczono limit czasu'),
        ('memory_limit', 'Przekroczono limit pamięci'),
        ('error', 'Błąd wykonania (Kompilacji/Runtime)'),
    ]

    # Relacje: Kto i co rozwiązuje?
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='solutions')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solutions')
    
    # Treść rozwiązania
    code = models.TextField(help_text="Kod źródłowy wysłany przez użytkownika")
    language = models.CharField(max_length=20, default='python')
    markdown_explanation = models.TextField(blank=True, null=True, help_text="Opcjonalny opis w Markdownie (HU 1.4)")
    
    # Wyniki sprawdzenia (wypełniane przez nasz przyszły system sprawdzający)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_time = models.IntegerField(blank=True, null=True, help_text="Czas wykonania w milisekundach (do statystyk HU 1.12)")
    memory_used = models.IntegerField(blank=True, null=True, help_text="Zużycie pamięci w kilobajtach (do statystyk HU 1.12)")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rozwiązanie {self.author.username} dla zadania: {self.task.title} ({self.get_status_display()})"
    
class CodeGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Nazwa grupy")
    description = models.TextField(blank=True, null=True, help_text="Opis grupy")
    
    # HU 2.2: Zmienianie dostępności grupy otwarta/zamknięta
    is_open = models.BooleanField(default=True, help_text="Czy grupa jest otwarta dla każdego?")
    
    # Relacja Wiele-do-Wielu przez naszą własną tabelę pośrednią
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='GroupMembership', 
        related_name='code_groups'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        typ = "Otwarta" if self.is_open else "Zamknięta"
        return f"{self.name} ({typ})"

class GroupMembership(models.Model):
    """
    Tabela pośrednia łącząca Użytkownika z Grupą.
    """
    ROLE_CHOICES = [
        ('member', 'Członek'),
        ('admin', 'Administrator Grupy'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(CodeGroup, on_delete=models.CASCADE)
    
    # Rola pozwala odróżnić zwykłego członka od admina grupy
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Zabezpieczenie na poziomie bazy danych: 
        # Jeden użytkownik może dołączyć do danej grupy tylko raz!
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} w {self.group.name} ({self.get_role_display()})"
    

class Contest(models.Model):
    """
    Model Konkursu - utworzont przez admina.
    """
    title = models.CharField(max_length=200, help_text="Nazwa konkursu")
    description = models.TextField(blank=True, null=True)
    
    # Konkurs jest przypisany do konkretnej grupy
    group = models.ForeignKey(CodeGroup, on_delete=models.CASCADE, related_name='contests')
    
    # Czas trwania konkursu
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # HU 2.3: Opcja zakazu przeglądania sieci (np. blokada wychodzenia z karty w React)
    strict_mode = models.BooleanField(default=False, help_text="Włącza restrykcje, np. zakaz kopiowania/opuszczania karty")
    
    # Konkurs ma wiele zadań, a zadanie może być w wielu konkursach (Many-to-Many)
    tasks = models.ManyToManyField(Task, related_name='contests')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.group.name})"


class TaskReport(models.Model):
    """
    Model zgłoszenia błędu w zadaniu (Tickety).
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Treść zgłoszenia (np. "W teście nr 3 wynik to 5, a nie 4")
    description = models.TextField(help_text="Szczegóły błędu w zadaniu")
    
    # Status zgłoszenia - pozwala adminowi śledzić i zamykać tickety
    is_resolved = models.BooleanField(default=False, help_text="Czy sprawa została rozwiązana?")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Rozwiązane" if self.is_resolved else "Otwarte"
        return f"Zgłoszenie do {self.task.title} od {self.reported_by.username} ({status})"