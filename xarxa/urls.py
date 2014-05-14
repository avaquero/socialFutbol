from django.conf.urls import patterns, url
from xarxa import views 

urlpatterns = patterns('',
    url(r'^tu$', views.generarPerfil, name='tu'),
    #url(r'^logout$', views.sortir, name='logout'),
)