# -*- coding: utf-8 -*-
from django import forms
from django.template.loader import render_to_string

from .models import Centro, Servicio, Equipo, Licencia, Trabajador


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
        labels = {'n_ir': 'Nº IR', 'categoriair': 'Categoria IR', }


class FormEquipo(forms.ModelForm):

    class Meta:
        model = Equipo
        fields = '__all__'


# Anade un boton de nuevo registro al desplegable
class SelectWithPop(forms.Select):

    def __init__(self, attrs=None, choices=()):
        super(SelectWithPop, self).__init__(attrs, choices)
        self.clave = ""

    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("sfmpr/popupplus.html", {'field': name, 'clave': self.clave})
        return html+popupplus


class FormLicencia(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormLicencia, self).__init__(*args, **kwargs)
        # En el caso de una nueva licencia
        # y almacena el valor para luego representarlo en HTML
        query_set = self.fields['servicio'].queryset
        if len(self.initial) > 0:
            if isinstance(self.initial['servicio'], basestring):   # Nueva licencia
                # cambia el desplegable de los servicios por un control invisible
                self.fields['servicio'].widget = forms.HiddenInput()
                id_servicio = int(self.initial['servicio'])
                self.text_servicio = query_set[id_servicio - 1]
                # además lo pasa al nuevo widget para volver luego a este punto
                self.fields['trabajador'].widget.clave = id_servicio

    class Meta:
        model = Licencia
        fields = '__all__'
        widgets = {'trabajador': SelectWithPop, 'tipo': forms.Select(
            choices=(('Operador', 'Operador'), ('Supervisor', 'Supervisor'), ))}


class FormTrabajador(forms.ModelForm):
    servicio = forms.CharField()

    def save(self, commit=True):
        key_field = self.cleaned_data.get('servicio', None)
        id = self.cleaned_data.get('nid', None)
        print key_field, id
        # ...do something with extra_field here...
        return super(FormTrabajador, self).save(commit=commit)

    class Meta:
        model = Trabajador
        fields = '__all__'
        labels = {'nid': 'NIF/Pasaporte', }
