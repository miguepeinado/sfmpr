# -*- coding: utf-8 -*-
from django import forms

from .models import Centro, Servicio, Equipo


class FormCentro(forms.ModelForm):

    class Meta:
        model = Centro
        fields = '__all__'


class DateInput(forms.DateInput):
    input_type = 'date'


class FormServicio(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {}
        labels = {'categoriair': 'Categoria IR',}


class FormEquipo(forms.ModelForm):

    class Meta:
        model = Equipo
        fields = '__all__'
        widgets = {}