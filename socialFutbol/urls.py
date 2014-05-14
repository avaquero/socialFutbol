from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'socialFutbol.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #URL per fer login
    url(r'^accedir/', include('perfils.urls', namespace='accedir')),
    #URL per mostrar el perfil
    url(r'^perfil/', include('xarxa.urls', namespace='perfil')),
)
