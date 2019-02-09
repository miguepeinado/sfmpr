# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# <----------------------------------- BASICO ------------------------------------->
# Poner alias a los campos y ver como usarlos
class Titular(models.Model):
    nif = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    dp = models.CharField(max_length=5)
    provincia = models.CharField(max_length=25, default='Asturias')
    siglas = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return self.nombre


class Centro(models.Model):
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE)
    area = models.CharField(max_length=5, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=10, null=True, blank=True)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    dp = models.CharField(max_length=5)
    provincia = models.CharField(max_length=25, default='Asturias')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(null=True, blank=True)

    def __unicode__(self):
        txt = u""
        if self.area is not None and len(self.area) > 0:
            txt = self.area + " - "
        txt += self.nombre
        return txt


    def servicios(self):
        return Servicio.objects.filter(centro=self)


class CategoriaIR(models.Model):
    categoria = models.CharField(max_length=100)

    def __unicode__(self):
        return self.categoria


class Servicio(models.Model):
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    # Datos de la IR en Industria/CSN
    n_ir = models.CharField(max_length=50, null=True, blank=True)
    expediente = models.CharField(max_length=50, null=True, blank=True)
    # Categoría según RIINNRR
    categoriair = models.ForeignKey(CategoriaIR, on_delete=models.CASCADE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(null=True, blank=True)

    def __unicode__(self):
        txt = self.nombre + ' (' + self.centro.__unicode__() + ')'
        return txt

    def codigo_completo(self):
        codigo = self.n_ir
        codigo += " (" + self.expediente + ")" if self.expediente is not None and len (self.expediente) > 0 else ""
        return codigo

    def contar_equipos(self):
        return Equipo.objects.filter(servicio=self).count()

    equipos = property(contar_equipos)


# <----------------------------------- EQUIPOS ------------------------------------->
class Modalidad(models.Model):
    siglas = models.CharField(max_length=10, null=True, blank=True)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        txt = self.nombre
        txt += " (" + self.siglas + ")" if self.siglas is not None and len(self.siglas) > 0 else ""
        return txt


class Equipo(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    sala = models.CharField(max_length=50)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    estudios = models.CharField(max_length=100, null=True, blank=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    n_serie = models.CharField(max_length=25, null=True, blank=True)
    n_sistema = models.CharField(max_length=25, null=True, blank=True)
    referencia = models.CharField(max_length=25, null=True, blank=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(null=True, blank=True)

    def __unicode__(self):
        txt = self.sala
        txt += " (" + self.referencia + ")" if self.referencia is not None and len(self.referencia) > 0 else ""
        return txt

    def marca_modelo(self):
        txt = self.marca + " " + self.modelo
        txt += " (N.S. " + self.n_serie + ")" if self.n_serie is not None and len(self.n_serie) > 0 else ""
        return txt


# <------------ TRABAJADOR (Valido para licencias y dosimetros) ------------>
class Titulacion(models.Model):
    codigo = models.CharField(max_length=50)
    titulacion = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.titulacion


class Trabajador(models.Model):
    # NIF/NIE/Pasaporte
    nid = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    domicilio = models.CharField(max_length=100, null=True, blank=True)
    cp = models.CharField(max_length=5, null=True, blank=True)
    localidad = models.CharField(max_length=50, null=True, blank=True)
    provincia = models.CharField(max_length=20, null=True, blank=True)
    titulacion = models.ForeignKey(Titulacion, null=True, blank=True, on_delete=models.CASCADE)

    def __unicode__(self):
        txt = self.nombre + ' ' + self.apellido1 + ' ' + self.apellido2
        return txt


# <---------------------------------- LICENCIAS -------------------------------->
class Licencia(models.Model):
    servicio = models.ManyToManyField(Servicio)
    tipo = models.CharField(max_length=10)
    numero = models.CharField(max_length=20)
    trabajador = models.ForeignKey(Trabajador, default=0, on_delete=models.CASCADE)
    fecha_concesion = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)

    def __unicode__(self):
        txt = self.numero + ' (' + self.tipo + ')'
        return txt