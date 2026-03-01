'''
Ten plik odpowiada za funkcje tłumaczące rekordy z bazy danych(które rozumie Django) na format JSON(który rozumie REACT)
'''
#region IMPORTY
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Snippet
# endregion IMPORTY

# Pobranie modelu użytkownika
User = get_user_model()

class SnippetSerializer(serializers.ModelSerializer):
    # To pole sprawi, że zamiast numerka ID autora, zobaczymy jego nazwę użytkownika
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Snippet
        # Wymieniamy pola, które chcemy wysłać do Reacta
        fields = ['id', 'title', 'code', 'language', 'author_name', 'created_at']

class RejestracjaSerializer(serializers.ModelSerializer):
    ''' Ta klasa ma za zadanie:
    1. Pobierac pola od frontendu(imie, role itd)
    2. Sprawdzac czy jezeli ktoś zaznaczył, że jest studentem to czy ma @student w mailu
    3. Poprawnie zapisać dane w bazie, używając funkcji szyfrującej hasło
    '''
    class Meta:
        '''
        Ta klasa mówi Django jakie pola z bazy danych go interesują
        '''

        model = User
        fields = ['username', 'email', 'password','first_name', 'last_name', 'rola', 'grupa_dziekanska', 'numer_indeksu']

        # Gdy API(Django) będzie odsyłać JSONa z odpowiedzą - password będzie z niego całkowicie wycięty
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        '''
        data - dictionary in Python

        Kiedy React wyśle JSONa do backendu ta funkcja uruchamia się automatycznie, zanim Django zapisze dane -> sprawdza wszystkie wpisane dane
        '''
        rola = data.get('rola', 'student')
        email = data.get('email', '')

        if rola == 'student':
            '''
            raise serializers.ValidationError - przerywa działanie i odsyła błąd w formacie JSON(kod 400 bad Request)
            '''

            # Zasada 1: Czy student ma domenę @student?
            if '@student' not in email:
                raise serializers.ValidationError({
                    "email": "Adres email studenta musi zawierać domenę @student."
                })
            

            # Zasada 2: Student musi mieć nr_indeksu oraz grupę
            if not data.get('numer_indeksu'):
                raise serializers.ValidationError({
                    "numer_indeksu": "Student musi podać numer indeksu."
                })
            if not data.get('grupa_dziekanska'):
                raise serializers.ValidationError({
                    "grupa_dziekanska": "Student musi mieć przypisaną grupę dziekańską."
                })
            
        elif rola == 'profesor':
            # Zasada 3: Profesor nie może mieć domeny @student
            if '@student' in email:
                raise serializers.ValidationError({
                    "email": "Konto profesorskie nie może być zarejestrowane na adres studencki."
                })
            # Czyszczenie: Jeśli ktoś sprytnie wysłał album jako profesor, ignorujemy to
            data['numer_indeksu'] = None
            data['grupa_dziekanska'] = None
        
        return data

    def create(self, validated_data):
        """
        Jeśli funkcja 'validate' przepuściła dane, ta funkcja tworzy użytkownika.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            rola=validated_data.get('rola', 'student'),
            grupa_dziekanska=validated_data.get('grupa_dziekanska', ''),
            numer_indeksu=validated_data.get('numer_indeksu', '')
        )
        return user
