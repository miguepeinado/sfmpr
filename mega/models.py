# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


# Poner alias a los campos y ver como usarlos
@python_2_unicode_compatible
class Titular(models.Model):
    nif = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    dp = models.CharField(max_length=5)
    provincia = models.CharField(max_length=25, default='Asturias')
    siglas = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
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

    def __str__(self):
        txt = ""
        if self.area is not None and len(self.area) > 0:
            txt = (self.area + " - ")
        txt += self.nombre
        return txt


@python_2_unicode_compatible
class CategoriaIR(models.Model):
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria


@python_2_unicode_compatible
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

    def __str__(self):
        return self.nombre

    def codigo_completo(self):
        codigo = self.n_ir
        codigo += " (" + self.expediente + ")" if self.expediente is not None and len (self.expediente) > 0 else ""
        return codigo

    def contar_equipos(self):
        return Equipo.objects.filter(servicio=self).count()

    equipos = property(contar_equipos)


@python_2_unicode_compatible
class Modalidad(models.Model):
    siglas = models.CharField(max_length=10, null=True, blank=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        txt = self.nombre
        txt += " (" + self.siglas + ")" if self.siglas is not None and len(self.siglas) > 0 else ""
        return txt


@python_2_unicode_compatible
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


    def __str__(self):
        txt = self.sala
        txt += " (" + self.referencia + ")" if self.referencia is not None and len(self.referencia) > 0 else ""
        return txt

    def marca_modelo(self):
        txt = self.marca + " " + self.modelo
        txt += " (N.S. " + self.n_serie + ")" if self.n_serie is not None and len(self.n_serie) > 0 else ""
        return txt