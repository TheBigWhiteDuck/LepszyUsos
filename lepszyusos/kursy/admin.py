from django.contrib import admin
from .models import Kurs


@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ('kod', 'nazwa', 'forma_zajec', 'ects', 'liczba_godzin', 'semestr', 'prowadzacy', 'limit_miejsc')
    list_filter = ('forma_zajec', 'semestr')
    search_fields = ('kod', 'nazwa', 'prowadzacy__last_name')
    filter_horizontal = ('studenci',)