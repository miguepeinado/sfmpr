# -*- coding: utf-8 -*-
from collections import OrderedDict
from django import forms

from .models import Centro, Servicio, Equipo, Licencia


class FormCentro(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormCentro, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        # Si se esta editando oculta el campo del titular
        if instance and instance.id:
            self.fields['titular'].widget = forms.HiddenInput()
            # y almacena el valor para luego representarlo en HTML
            query_set = self.fields['titular'].queryset
            self.text_titular = query_set[self['titular'].value() - 1]

    class Meta:
        model = Centro
        fields = '__all__'


class FormServicio(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormServicio, self).__init__(*args, **kwargs)
        # cambia el desplegable de los centros por un control invisible
        self.fields['centro'].widget = forms.HiddenInput()
        # y almacena el valor para luego representarlo en HTML
        query_set = self.fields['centro'].queryset
        self.text_centro = query_set[self['centro'].value() - 1]


    class Meta:
        model = Servicio
        fields = '__all__'
        labels = {'n_ir':'Nº IR', 'categoriair': 'Categoria IR',}


class FormEquipo(forms.ModelForm):

    class Meta:
        model = Equipo
        fields = '__all__'


class FormLicencia(forms.ModelForm):

    class Meta:
        model = Licencia
        fields = '__all__'