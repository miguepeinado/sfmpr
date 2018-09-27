# -*- coding: utf-8 -*-
from django import forms

from .models import Centro, Servicio


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