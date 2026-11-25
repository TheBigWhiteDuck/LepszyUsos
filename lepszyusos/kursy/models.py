from django.conf import settings
from django.db import models


class Kurs(models.Model):
    class FormaZajec(models.TextChoices):
        WYKLAD = 'wyklad', 'Wykład'
        LABORATORIA = 'laboratoria', 'Laboratoria'
        CWICZENIA = 'cwiczenia', 'Ćwiczenia'
        SEMINARIUM = 'seminarium', 'Seminarium'

    nazwa = models.CharField('nazwa przedmiotu', max_length=150)
    kod = models.CharField('kod kursu', max_length=20, unique=True)
    forma_zajec = models.CharField(
        'forma zajęć',
        max_length=20,
        choices=FormaZajec.choices,
        default=FormaZajec.WYKLAD,
    )
    ects = models.PositiveSmallIntegerField('punkty ECTS', default=3)
    liczba_godzin = models.PositiveSmallIntegerField('liczba godzin', default=30)
    semestr = models.CharField('semestr', max_length=30, help_text='Np. 2026/2027Z')
    opis = models.TextField('opis i warunki zaliczenia', blank=True)
    limit_miejsc = models.PositiveIntegerField('limit miejsc', default=30)

    prowadzacy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prowadzone_kursy',
        verbose_name='prowadzący',
    )
    studenci = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='zapisane_kursy',
        verbose_name='zapisani studenci',
    )
    utworzono = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'kurs'
        verbose_name_plural = 'kursy'
        ordering = ['nazwa']

    def __str__(self):
        return f'{self.kod} – {self.nazwa} ({self.get_forma_zajec_display()})'

    @property
    def liczba_studentow(self):
        return self.studenci.count()

    @property
    def czy_pelny(self):
        return self.liczba_studentow >= self.limit_miejsc
        
    @property
    def kolor_formy(self):
        kolory = {
            self.FormaZajec.WYKLAD: 'text-bg-primary',
            self.FormaZajec.CWICZENIA: 'text-bg-warning',
            self.FormaZajec.LABORATORIA: 'text-bg-success',
            self.FormaZajec.SEMINARIUM: 'text-bg-dark',
        }
        return kolory.get(self.forma_zajec, 'text-bg-secondary')