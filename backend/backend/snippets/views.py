from django.shortcuts import render, redirect, get_object_or_404
from .models import Snippet
from .forms import SnippetForm, RejestracjaForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

#Z Django Rest Framework(DRF)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SnippetSerializer
from rest_framework import viewsets
from .serializers import SnippetSerializer


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

# ----- Sekcja API -----
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