# Kod ten tłumaczy rekordy z bazy danych(które rozumie Django) na format JSON(który rozumie REACT)
from rest_framework import serializers
from .models import Snippet

class SnippetSerializer(serializers.ModelSerializer):
    # To pole sprawi, że zamiast numerka ID autora, zobaczymy jego nazwę użytkownika
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Snippet
        # Wymieniamy pola, które chcemy wysłać do Reacta
        fields = ['id', 'title', 'code', 'language', 'author_name', 'created_at']