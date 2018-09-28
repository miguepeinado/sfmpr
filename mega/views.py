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


class Mensaje:
    """
    Only for log purposes
    """
    titulo = "28/09/09: Implementar migracion de la base de datos de IIRR"
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
    from .models import Centro, Titular, CategoriaIR, Servicio

    mensaje = Mensaje()
    """
    try:
        cursor = connections['legacy_ir'].cursor()
        # Importar titulares
        sql = "SELECT * FROM IIRR"
        cursor.execute(sql)
        for row in cursor.fetchall():
            try:
                centro = Centro.objects.get(id=row[2])
            except ObjectDoesNotExist:
                mensaje.add_mess("FAIL: Centro not found with id %s" % row[2])
            try:
                cat = row[5] if row[5] != 1 else 4
                mensaje.add_mess(">>> Categoria_ir index changed from 1 to 4")
                categoriair = CategoriaIR.objects.get(id=cat)
            except ObjectDoesNotExist:
                mensaje.add_mess("FAIL: Categoria not found with id %s" % row[2])
                continue
            else:
                try:
                    alta = datetime.date(row[6])
                    mensaje.add_mess("Date imported: %s" % row[2])
                except:
                    alta = timezone.now()
                servicio = Servicio(id=row[0], nombre=row[1], centro=centro, n_ir=row[3], expediente=row[4],
                                    categoriair=categoriair, fecha_alta=alta, fecha_baja=row[8])
                print row[1], row[3], alta
                servicio.save()
                mensaje.add_mess("> Servicio '" + row[1] + "' added to sfmpr database")

    except ConnectionDoesNotExist:
        mensaje.add_mess("FAIL: Legacy database is not configured")
        cursor = None
    """
    return render(request, 'sfmpr/otros.html', {'mensaje': mensaje})