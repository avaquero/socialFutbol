# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from perfils.models import Perfil
from xarxa.models import Publicacio, Comentari

# Create your views here.
def generarPerfil(request):
    perfil = request.user.perfil
    publicacions = Publicacio.objects.filter(usuari = perfil)
    
    context = {'perfil':perfil, 'publicacions':publicacions}
    return render(request, 'tu.html', context)