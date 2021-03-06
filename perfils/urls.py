from django.conf.urls import patterns, url
from perfils import views 

urlpatterns = patterns('',
    url(r'^$', views.entrar, name='login'),
    url(r'^logout$', views.sortir, name='logout'),
    url(r'^registrarse', views.registrarse, name='registrarse'),
    url(r'^dadesPerfil', views.modificarDadesPerfil, name='modificarDades'),
    url(r'^canviPass', views.canviaContrasenya, name='canviPass'),
    url(r'^backup', views.copiaSeguretat, name='backup'),  
)