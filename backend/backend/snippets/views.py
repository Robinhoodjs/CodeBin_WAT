# region importy DJANGO
from django.shortcuts import render, redirect, get_object_or_404
from .models import Snippet
from .forms import SnippetForm, RejestracjaForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
# endregion importy DJANGO

# region importy Z Django Rest Framework(DRF)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SnippetSerializer
from rest_framework import viewsets, status
from .serializers import SnippetSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RejestracjaSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
# endregion importy Z Django Rest Framework(DRF)

User = get_user_model()

# region FUNKCJE
@login_required
def snippet_list(request):
    if request.user.is_teacher or request.user.is_superuser:
        snippets = Snippet.objects.all().order_by('-created_at')
    else:
        snippets = Snippet.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'lista_snippetow': snippets
    }
    
    return render(request, 'snippets/snippet_list.html', context)

@login_required
def snippet_new(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            # Zatrzymujemy automatyczny zapis formularza
            snippet = form.save(commit=False)
            
            # przypisanie autora
            snippet.author = request.user
            snippet.save()

            return redirect('lista_kodow')
    else:
        form = SnippetForm()
    
    return render(request, 'snippets/snippet_edit.html', {'form': form})

def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if snippet.author != request.user and not request.user.is_teacher and not request.user.is_superuser:
        raise PermissionDenied("Brak dostępu do kodu innego użytkownika")

    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})

def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RejestracjaForm()

    return render(request, 'registration/rejestracja.html', {'form': form})

@login_required
def snippet_edit_view(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if snippet.author != request.user:
        raise PermissionDenied("Nie możesz edytować cudzego rozwiązania.")

    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('szczegoly_kodu', pk=snippet.pk)
    else:
        form = SnippetForm(instance=snippet)

    return render(request, 'snippets/snippet_edit.html', {'form': form, 'tryb_edycji': True})

@login_required
def snippet_delete(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if snippet.author != request.user:
        raise PermissionDenied("Nie możesz edytować cudzego rozwiązania.")
    
    if request.method == "POST":
        snippet.delete()
        return redirect('lista_kodow')
        
    return render(request, 'snippets/snippet_confirm_delete.html', {'snippet': snippet})
# endregion FUNKCJE

# region Funkcje Sekcja API
class SnippetViewSet(viewsets.ModelViewSet):
    """
    Ten jeden ViewSet automatycznie generuje nam:
    - GET /api/kody/ (Lista wszystkich)
    - POST /api/kody/ (Dodawanie nowego)
    - GET /api/kody/5/ (Pobieranie jednego)
    - PUT /api/kody/5/ (Edycja)
    - DELETE /api/kody/5/ (Usuwanie)
    """
    queryset = Snippet.objects.all().order_by('-created_at')
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] #    IsAuthenticatedOrReadOnly - [GET] pozwala każdemu(niezalogowanym też) na pobranie i obejrzenie listy kodów, jednak nie pozwala na POST, PUT, DELETE


    def perform_create(self, serializer):
        '''
        Ta funkcja sprawdza token uwierzytelniania w Headerze i na jego podstawie przypisuje kod właściwemu autorowi
        '''
        # self.request.user to obiekt użytkownika, którego Django rozpoznało po Tokenie!
        serializer.save(author=self.request.user)

class RejestracjaView(generics.CreateAPIView):
    """
    Endpoint pozwalający na rejestrację nowego użytkownika.
    Przyjmuje POST z danymi: username, email, password.
    """
    queryset = User.objects.all()
    serializer_class = RejestracjaSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"wiadomosc": "Konto zostało pomyślnie utworzone."},
            status=status.HTTP_201_CREATED
        )

# endregion Funkcje Sekcja API