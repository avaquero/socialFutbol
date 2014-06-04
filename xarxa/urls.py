from django.conf.urls import patterns, url
from xarxa import views 

urlpatterns = patterns('',
    url(r'^tu$', views.generarPerfil, name='tu'),
    url(r'^(?P<idPerfil>\d+)$', views.veurePerfil, name='perfilAjeno'),
    url(r'^nouAmic/(?P<idPerfil>\d+)$', views.afegirAmic, name='nouAmic'),
    url(r'^acceptarAmic/(?P<idLinea>\d+)$', views.acceptarAmic, name='acceptarAmic'),
    url(r'^eliminar/(?P<idLinea>\d+)$', views.eliminarSolicitud, name='eliminarAmic'),
    url(r'^modificaPub/(?P<idPublicacio>\d+)$', views.modificaPublicacio, name='modificar'),
    url(r'^eliminaPub/(?P<idPublicacio>\d+)$', views.eliminaPublicacio, name='eliminar'),
    url(r'^buscar$', views.perfils, name='perfil'),
#     url(r'^perfilAltreAjax$', views.perfilAltreAjax, name='perfilAltreAjax'),
#     url(r'^comentarisAjax$', views.comentarisAjax, name='comentarisAjax'),
#     url(r'^comentarisPerfil$', views.perfilAjax, name='comentarisPerfil'),
#     url(r'^perfilTuAjax$', views.perfilTuAjax, name='perfilTuAjax'),
    url(r'^publicacio/(?P<idPub>\d+)', views.compartirPub, name='compartirPub'),
    #url(r'^logout$', views.sortir, name='logout'),
)