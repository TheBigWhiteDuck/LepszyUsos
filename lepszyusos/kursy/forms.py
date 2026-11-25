from django import forms
from accounts.forms import BootstrapMixin
from accounts.models import User
from .models import Kurs


class KursForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Kurs
        fields = (
            'kod',
            'nazwa',
            'forma_zajec',
            'ects',
            'liczba_godzin',
            'semestr',
            'limit_miejsc',
            'opis',
        )
        widgets = {
            'opis': forms.Textarea(attrs={'rows': 4}),
        }

class PrzypiszStudentaForm(BootstrapMixin, forms.Form):
    nr_albumu = forms.CharField(
        label='Numer albumu studenta',
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'np. 123456'}),
    )

    def __init__(self, *args, kurs=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.kurs = kurs
        self.student = None

    def clean_nr_albumu(self):
        nr = self.cleaned_data['nr_albumu'].strip()
        try:
            student = User.objects.get(nr_albumu=nr, role=User.Role.STUDENT, is_superuser=False)
        except User.DoesNotExist:
            raise forms.ValidationError('Nie znaleziono studenta o podanym numerze albumu.')

        if self.kurs and self.kurs.studenci.filter(pk=student.pk).exists():
            raise forms.ValidationError('Ten student jest już zapisany na ten kurs.')

        if self.kurs and self.kurs.czy_pelny:
            raise forms.ValidationError('Osiągnięto limit miejsc na tym kursie.')

        self.student = student
        return nr