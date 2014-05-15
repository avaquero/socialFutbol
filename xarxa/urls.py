from django.conf.urls import patterns, url
from xarxa import views 

urlpatterns = patterns('',
    url(r'^tu$', views.generarPerfil, name='tu'),
    url(r'^perfilAgeno/(?P<idPerfil>\d+)$', views.veurePerfil, name='perfilAgeno'),
    url(r'^nouAmic/(?P<idPerfil>\d+)$', views.afegirAmic, name='nouAmic'),
    #url(r'^logout$', views.sortir, name='logout'),
)