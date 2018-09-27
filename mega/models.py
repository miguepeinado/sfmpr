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
    siglas = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Centro(models.Model):
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE)
    area = models.CharField(max_length=5, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    dp = models.CharField(max_length=5)
    provincia = models.CharField(max_length=25, default='Asturias')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(null=True, blank=True)

    def __str__(self):
        txt = (self.area + " - ") if len(self.area) > 0 else ""
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
    n_ir = models.CharField(max_length=50, null=True, blank=True)
    expediente = models.CharField(max_length=50, null=True, blank=True)
    categoriair = models.ForeignKey(CategoriaIR, on_delete=models.CASCADE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre