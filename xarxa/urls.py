from django.conf.urls import patterns, url
from xarxa import views 

urlpatterns = patterns('',
    url(r'^tu$', views.generarPerfil, name='tu'),
    url(r'^(?P<idPerfil>\d+)$', views.veurePerfil, name='perfilAjeno'),
    url(r'^nouAmic/(?P<idPerfil>\d+)$', views.afegirAmic, name='nouAmic'),
    url(r'^acceptarAmic/(?P<idLinea>\d+)$', views.acceptarAmic, name='acceptarAmic'),
    #url(r'^logout$', views.sortir, name='logout'),
)