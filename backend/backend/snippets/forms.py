from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Snippet, Uzytkownik

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['title', 'code', 'language']
        labels = {
            'title': 'Tytuł',
            'code': 'Twój kod',
            'language': 'Język programowania'
        }

class RejestracjaForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Uzytkownik
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'numer_indeksu', 'grupa_dziekanska')

        labels = {
            'first_name': "Imię",
            'last_name': "Nazwisko",
            'numer_indeksu': "Numer Indeksu",
            'grupa_dziekanska': "Grupa Dziekańska"
        }