# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# Register your models here.
from .models import Titular, CategoriaIR, Modalidad

admin.site.register(Titular)
admin.site.register(CategoriaIR)
admin.site.register(Modalidad)