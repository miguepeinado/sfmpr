# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(Titular)
admin.site.register(CategoriaIR)
admin.site.register(Modalidad)
admin.site.register(Centro)
admin.site.register(Servicio)
admin.site.register(Licencia)
admin.site.register(Titulacion)
admin.site.register(Trabajador)