# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.forms.widgets import DateInput
from .models import Centro, Servicio, Equipo
from .forms import FormCentro, FormServicio, FormEquipo


def datos(model_instance):
    _datos = OrderedDict()
    for f in model_instance._meta.fields:
        if f.name != "id":
            key = f.name.capitalize()
            # if key.split("_")[0]=="N":
            #     key = key.replace(key[0:key.find("_")], "Nº")
            key = key.replace("_", " ")
            _datos[key] = getattr(model_instance, f.name, None)
            if _datos[key] is None:
                _datos[key] = ""
    return _datos


def lista_centros(request):
    centros = Centro.objects.all().order_by('area', 'nombre')
    return render(request, 'sfmpr/lista_centros.html', {'centros': centros,})


def ver_centro(request, pk):
        centro = get_object_or_404(Centro, pk=pk)
        return render(request, 'sfmpr/ver_centro.html', {'centro': centro, 'datos': datos(centro)})


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
    return render(request, 'sfmpr/ver_servicio.html', {'servicio': servicio, 'datos': datos(servicio)})


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


def lista_equipos(request, fk):
    equipos = Equipo.objects.filter(servicio=fk).order_by('referencia')
    servicio = Servicio.objects.filter(id=fk)[0]
    return render(request, 'sfmpr/lista_equipos.html', {'equipos': equipos, 'servicio': servicio})


def ver_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    return render(request, 'sfmpr/ver_equipo.html', {'equipo': equipo, 'datos': datos(equipo)})


def nuevo_equipo(request, fk):
    if request.method == "POST":
        form = FormEquipo(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.save()
        return redirect('ver_equipo', pk=equipo.pk)
    else:
        form = FormEquipo(initial={'servicio': fk})
        form._meta.widgets['fecha_alta']=DateInput()
    return render(request, 'sfmpr/nuevo_equipo.html', {'form': form})


def editar_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == "POST":
        form = FormEquipo(request.POST, instance=equipo)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.author = request.user
            equipo.save()
        return redirect('ver_equipo', pk=equipo.pk)
    else:
        form = FormEquipo(instance=equipo)
    return render(request, 'sfmpr/nuevo_equipo.html', {'form': form})


class Mensaje:
    """
    Only for log purposes
    """
    titulo = "29/09/09: Implementar migracion de las base de datos anteriores"
    descripcion = "<p>Cargar en la base de datos del sitio las filas de la base de datos de mi ordenador</p>"

    def add_mess(self, msg):
        Mensaje.descripcion += "<p>" + msg + "</p>"


def otros(request):
    """
    Importar una tabla de la base de datos anterior cuando pulsamos un boton
    (Ver http://jantoniomartin.tumblr.com/post/15233766067/django-how-to-import-data-from-an-external)
    """
    from django.db import connections
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.utils import ConnectionDoesNotExist
    from django.utils import timezone
    from datetime import datetime
    from .models import Servicio, Equipo, Modalidad
    """
    mensaje = Mensaje()
    try:
        cursor = connections['legacy_equipos'].cursor()
        # Importar equipos
        sql = "SELECT * FROM Equipos"
        cursor.execute(sql)
        for row in cursor.fetchall():
            try:
                servicio = Servicio.objects.get(id=row[1])
                modalidad = Modalidad.objects.get(id=1)
            except ObjectDoesNotExist:
                mensaje.add_mess("FAIL: Servicio not found with id %s" % row[1])
            else:
                equipo = Equipo(id=row[0], servicio=servicio, sala=row[2], modalidad=modalidad, marca=row[5],
                                modelo=row[6], n_serie=row[7], n_sistema=row[8], referencia=row[11])
                equipo.save()
                mensaje.add_mess("> Equipo '" + row[2] + "' added to sfmpr database")

    except ConnectionDoesNotExist:
        mensaje.add_mess("FAIL: Legacy database is not configured")
        cursor = None
    return render(request, 'sfmpr/otros.html', {'mensaje': mensaje})
    """