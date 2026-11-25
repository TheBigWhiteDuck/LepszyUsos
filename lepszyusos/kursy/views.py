from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import tylko_prowadzacy
from accounts.models import User
from .forms import KursForm, PrzypiszStudentaForm
from .models import Kurs


@tylko_prowadzacy
def panel_prowadzacego(request):
    kursy = Kurs.objects.filter(prowadzacy=request.user)
    return render(request, 'kursy/panel.html', {'kursy': kursy})


@tylko_prowadzacy
def dodaj_kurs(request):
    form = KursForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        kurs = form.save(commit=False)
        kurs.prowadzacy = request.user
        kurs.save()
        messages.success(request, f'Utworzono kurs „{kurs.nazwa}”.')
        return redirect('szczegoly_kursu', pk=kurs.pk)
    return render(request, 'kursy/kurs_form.html', {'form': form, 'tytul': 'Nowy kurs'})


@tylko_prowadzacy
def edytuj_kurs(request, pk):
    kurs = get_object_or_404(Kurs, pk=pk, prowadzacy=request.user)
    form = KursForm(request.POST or None, instance=kurs)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Zapisano zmiany w kursie.')
        return redirect('szczegoly_kursu', pk=kurs.pk)
    return render(request, 'kursy/kurs_form.html', {'form': form, 'kurs': kurs, 'tytul': 'Edycja kursu'})


@tylko_prowadzacy
def usun_kurs(request, pk):
    kurs = get_object_or_404(Kurs, pk=pk, prowadzacy=request.user)
    if request.method == 'POST':
        nazwa = kurs.nazwa
        kurs.delete()
        messages.success(request, f'Usunięto kurs „{nazwa}”.')
        return redirect('panel_prowadzacego')
    return render(request, 'kursy/kurs_usun.html', {'kurs': kurs})


@tylko_prowadzacy
def szczegoly_kursu(request, pk):
    kurs = get_object_or_404(Kurs, pk=pk, prowadzacy=request.user)
    form = PrzypiszStudentaForm(request.POST or None, kurs=kurs)

    if request.method == 'POST' and form.is_valid():
        kurs.studenci.add(form.student)
        messages.success(request, f'Dodano studenta: {form.student} ({form.student.nr_albumu}).')
        return redirect('szczegoly_kursu', pk=kurs.pk)

    studenci = kurs.studenci.order_by('last_name', 'first_name')
    return render(request, 'kursy/szczegoly_kursu.html', {
        'kurs': kurs,
        'studenci': studenci,
        'form': form,
    })


@tylko_prowadzacy
@require_POST
def wypisz_studenta(request, pk, student_pk):
    kurs = get_object_or_404(Kurs, pk=pk, prowadzacy=request.user)
    student = get_object_or_404(User, pk=student_pk)
    kurs.studenci.remove(student)
    messages.info(request, f'Usunięto studenta {student} z kursu.')
    return redirect('szczegoly_kursu', pk=kurs.pk)