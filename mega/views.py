# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.forms.widgets import DateInput
from .models import Centro, Servicio
from .forms import FormCentro, FormServicio


def lista_centros(request):
    centros = Centro.objects.all().order_by('area', 'nombre')
    return render(request, 'sfmpr/lista_centros.html', {'centros': centros})


def ver_centro(request, pk):
    centro = get_object_or_404(Centro, pk=pk)
    return render(request, 'sfmpr/ver_centro.html', {'centro': centro})


def nuevo_centro(request):
    if request.method == "POST":
        form = FormCentro(request.POST)
        if form.is_valid():
            centro = form.save(commit=False)
            centro.save()
        return redirect('ver_centro', pk=centro.pk)
    else:
        form = FormCentro()
    return render(request, 'sfmpr/nuevo_centro.html', {'form': form})


def editar_centro(request, pk):
    centro = get_object_or_404(Centro, pk=pk)
    if request.method == "POST":
        form = FormCentro(request.POST, instance=centro)
        if form.is_valid():
            centro = form.save(commit=False)
            centro.author = request.user
            centro.save()
        return redirect('ver_centro', pk=centro.pk)
    else:
        form = FormCentro(instance=centro)
    return render(request, 'sfmpr/nuevo_centro.html', {'form': form})


def lista_servicios(request, fk):
    servicios = Servicio.objects.filter(centro=fk).order_by('nombre')
    centro = Centro.objects.filter(id=fk)[0]
    return render(request, 'sfmpr/lista_servicios.html', {'servicios': servicios, 'centro': centro})


def ver_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    return render(request, 'sfmpr/ver_servicio.html', {'servicio': servicio})


def nuevo_servicio(request, fk):
    if request.method == "POST":
        form = FormServicio(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.save()
        return redirect('ver_servicio', pk=servicio.pk)
    else:
        form = FormServicio(initial={'centro': fk})
        form._meta.widgets['fecha_alta']=DateInput()
    return render(request, 'sfmpr/nuevo_servicio.html', {'form': form})


def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == "POST":
        form = FormServicio(request.POST, instance=servicio)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.author = request.user
            servicio.save()
        return redirect('ver_servicio', pk=servicio.pk)
    else:
        form = FormServicio(instance=servicio)
    return render(request, 'sfmpr/nuevo_servicio.html', {'form': form})