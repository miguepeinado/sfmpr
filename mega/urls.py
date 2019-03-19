from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Primera pagina...cambiar cuando pidamos ingresar con usuario
    url(r'^$', views.lista_centros, name='lista_centros'),
    # centros
    url(r'^nuevo_centro/$', views.NuevoCentro.as_view(), name='nuevo_centro'),
    url(r'^ver_centro/(?P<pk>[0-9]+)/$', views.ver_centro, name='ver_centro'),
    url(r'^editar_centro/(?P<pk>[0-9]+)/$', views.EditarCentro.as_view(), name='editar_centro'),
    # servicios
    url(r'^nuevo_servicio/(?P<fk>[0-9]+)/$', views.NuevoServicio.as_view(), name='nuevo_servicio'),
    url(r'^ver_servicio/(?P<pk>[0-9]+)/$', views.ver_servicio, name='ver_servicio'),
    url(r'^editar_servicio/(?P<pk>[0-9]+)/$', views.EditarServicio.as_view(), name='editar_servicio'),
    # Equipos
    url(r'^sfmpr/lista_equipos/(?P<fk>[0-9]+)/$', views.lista_equipos, name='lista_equipos'),
    url(r'^sfmpr/nuevo_equipo/(?P<fk>[0-9]+)/$', views.nuevo_equipo, name='nuevo_equipo'),
    url(r'^equipo/(?P<pk>[0-9]+)/$', views.ver_equipo, name='ver_equipo'),
    url(r'^equipo/(?P<pk>[0-9]+)/editar/$', views.editar_equipo, name='editar_equipo'),
    # Licencias
    url(r'^lista_licencias/(?P<fk>[0-9]+)/$', views.lista_licencias, name='lista_licencias'),
    url(r'^ver_licencia/(?P<pk>[0-9]+)/$', views.ver_licencia, name='ver_licencia'),
    url(r'^editar_licencia/(?P<pk>[0-9]+)/$', views.EditarLicencia.as_view(), name='editar_licencia'),
    url(r'^nueva_licencia/(?P<fk>[0-9]+)/$', views.NuevaLicencia.as_view(), name='nueva_licencia'),
    # Trabajadores
    url(r'^ver_trabajador/(?P<pk>[0-9]+)/$', views.ver_trabajador, name='ver_trabajador'),
    url(r'^editar_trabajador/(?P<pk>[0-9]+)/$', views.EditarTrabajador.as_view(), name='editar_trabajador'),
    url(r'^nuevo_trabajador/$', views.NuevoTrabajador.as_view(), name='nuevo_trabajador'),
    # otros
    url(r'^otros/$', views.otros, name='otros'),
    url(r'^ayuda/$', views.ayuda, name='ayuda'),
]