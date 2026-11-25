from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_prowadzacego, name='panel_prowadzacego'),
    path('nowy/', views.dodaj_kurs, name='dodaj_kurs'),
    path('<int:pk>/', views.szczegoly_kursu, name='szczegoly_kursu'),
    path('<int:pk>/edytuj/', views.edytuj_kurs, name='edytuj_kurs'),
    path('<int:pk>/usun/', views.usun_kurs, name='usun_kurs'),
    path('<int:pk>/wypisz/<int:student_pk>/', views.wypisz_studenta, name='wypisz_studenta'),
]