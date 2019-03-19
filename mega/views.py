# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
import copy

from django.views.generic.edit import FormView, UpdateView, CreateView
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.forms.widgets import DateInput
from .models import Centro, Servicio, Equipo, Licencia, Trabajador
from django.db.models.fields.related import ManyToManyField
from .forms import FormCentro, FormServicio, FormEquipo, FormLicencia, FormTrabajador


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


def datos(model_instance, initial_data = None, labels = {}, id_included=False):
    _datos = initial_data if isinstance(initial_data, OrderedDict) else OrderedDict()
    for f in model_instance._meta.get_fields():
        # Do not include:
        # Field id except if wanted
        # Model fields that have this as a key
        # Many2many fields
        if (f.name != "id" or id_included) and not f.auto_created and not isinstance(f, ManyToManyField):
            key = f.name
            if key in labels:
                key = labels[key]
            else:
                key = key.capitalize()
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


class NuevoCentro(CreateView):
    template_name = 'sfmpr/centro.html'
    form_class = FormCentro
    success_url = reverse_lazy('lista_centros')


class EditarCentro(UpdateView):
    model = Centro
    template_name = 'sfmpr/centro.html'
    form_class = FormCentro
    success_url = reverse_lazy('lista_centros')


# <--------------------->
def ver_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    return render(request, 'sfmpr/ver_servicio.html', {'servicio': servicio, 'datos': datos(servicio)})


class NuevoServicio(CreateView):
    template_name = 'sfmpr/servicio.html'
    form_class = FormServicio
    success_url = reverse_lazy('lista_centros')

    def get_initial(self):
        fk = int(self.request.resolver_match.kwargs['fk'])
        return {'centro': fk}


class EditarServicio(UpdateView):
    model = Servicio
    template_name = 'sfmpr/servicio.html'
    form_class = FormServicio
    success_url = reverse_lazy('lista_centros')

# <----------------------->

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


# <------------------------------------>
def lista_licencias(request, fk):
    licencias = Licencia.objects.filter(servicio=fk)
    servicio = Servicio.objects.filter(id=fk)[0]
    return render(request, 'sfmpr/lista_licencias.html', {'licencias': licencias, 'servicio': servicio})


def ver_licencia(request, pk):
    licencia = get_object_or_404(Licencia, pk=pk)
    s = u""
    for element in licencia.servicio.values('nombre'):
        s += element['nombre'] + "\n"

    inicial = OrderedDict()
    inicial['Servicio(s)'] = s
    return render(request, 'sfmpr/ver_licencia.html', {'licencia': licencia, 'datos': datos(licencia, initial_data=inicial), })


class NuevaLicencia(CreateView):
    template_name = 'sfmpr/licencia.html'
    form_class = FormLicencia


    def get_initial(self):
        fk = self.request.resolver_match.kwargs['fk']
        return {'servicio': fk, }

    def post(self, request, *args, **kwargs):
        form = FormLicencia(request.POST)
        if form.is_valid():
            licencia = form.save()
            licencia.save()         # Redundant
            return redirect(self.request.META.get('HTTP_REFERER'))
        return super(NuevaLicencia, self).post(request, *args, **kwargs)


class EditarLicencia(UpdateView):
    model = Licencia
    template_name = 'sfmpr/licencia.html'
    form_class = FormLicencia

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


def ver_trabajador(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    labels = {'nid': u'NIF/Pasaporte', 'apellido1': u'Apellido 1', 'apellido2': u'Apellido 2',
              'telefono': u'Teléfono', 'cp': u'Código postal', 'titulacion': u'Titulación', }
    return render(request, 'sfmpr/ver_trabajador.html', {'trabajador': trabajador,
                                                         'datos': datos(trabajador, labels=labels)})


class NuevoTrabajador(CreateView):
    # todo: Seleccionar fk trabajador en el formulario licencia con los datos del nuevo trabajador
    template_name = 'sfmpr/trabajador.html'
    form_class = FormTrabajador

    def post(self, request, *args, **kwargs):
        form = FormTrabajador(request.POST)
        if form.is_valid():
            trabajador = form.save()
            trabajador.save()
            return redirect(self.request.META.get('HTTP_REFERER'))
        return super(NuevoTrabajador, self).post(request, *args, **kwargs)

    # def get_success_url(self):
    #     return self.request.META.get('HTTP_REFERER')


class EditarTrabajador(UpdateView):
    model = Trabajador
    template_name = 'sfmpr/trabajador.html'
    form_class = FormTrabajador

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


def ayuda(request):
    return render(request, "sfmpr/ayuda.html")


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