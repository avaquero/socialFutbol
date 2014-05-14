from django.conf.urls import patterns, url
from perfils import views 

urlpatterns = patterns('',
    url(r'^login$', views.entrar, name='login'),
    url(r'^logout$', views.sortir, name='logout'),
)