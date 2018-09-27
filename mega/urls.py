from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Primera pagina...cambiar cuando pidamos ingresar con usuario
    url(r'^$', views.lista_centros),
    # centros
    url(r'^sfmpr/nuevo_centro/$', views.nuevo_centro, name='nuevo_centro'),
    url(r'^centro/(?P<pk>[0-9]+)/$', views.ver_centro, name='ver_centro'),
    url(r'^centro/(?P<pk>[0-9]+)/editar/$', views.editar_centro, name='editar_centro'),
    # servicios
    url(r'^sfmpr/lista_servicios/(?P<fk>[0-9]+)/$', views.lista_servicios, name='lista_servicios'),
    url(r'^sfmpr/nuevo_servicio/(?P<fk>[0-9]+)/$', views.nuevo_servicio, name='nuevo_servicio'),
    url(r'^servicio/(?P<pk>[0-9]+)/$', views.ver_servicio, name='ver_servicio'),
    url(r'^servicio/(?P<pk>[0-9]+)/editar/$', views.editar_servicio, name='editar_servicio'),
]