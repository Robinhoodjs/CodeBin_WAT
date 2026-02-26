from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Tworzymy automatyczny ruter z DRF
router = DefaultRouter()
# 2. Rejestrujemy w nim naszą nową klasę pod nazwą 'kody'
router.register(r'kody', views.SnippetViewSet, basename='snippet')

urlpatterns = [
    path('', views.snippet_list, name='lista_kodow'),
    path('nowy/', views.snippet_new, name='nowy_kod'),
    path('<int:pk>/', views.snippet_detail, name='szczegoly_kodu'),
    path('<int:pk>/edytuj/', views.snippet_edit_view, name='edytuj_kod'),
    path('<int:pk>/usun/', views.snippet_delete, name='usun_kod'),
    
    # --- NOWE GŁÓWNE API ---
    # Podpinamy wszystkie wygenerowane ścieżki pod adres /api/
    path('api/', include(router.urls)),
]