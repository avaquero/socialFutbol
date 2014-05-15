# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from perfils.models import Perfil, Amic
from xarxa.models import Publicacio, Comentari
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import datetime

# Create your views here.
#GENERAR EL TEU PERFIL
def generarPerfil(request):
    perfil = request.user.perfil
    publicacions = Publicacio.objects.filter(usuari = perfil)
    peticions = Amic.objects.filter(usuariAmic = perfil, acceptat = 0)
    
    #mevaPeticio = Amic.objects.get(usuari_id)
    
    #eticioDe = Perfil.objects.filter(usuari = mevaPeticio)
    
    for peticio in peticions:
        print peticio.usuari_id
        user_act = Perfil.objects.get(usuari = peticio.usuari_id)
        print user_act.nom + " " + user_act.cognoms
        #emmagatzemar en una llista / array
    
    context = {'perfil':perfil, 'publicacions':publicacions, 'peticions':peticions }
    return render(request, 'tu.html', context)

#GENERAR PERFIL D'aLTRES
def veurePerfil(request, idPerfil):
    perfil = get_object_or_404(Perfil, pk=idPerfil)
    publicacions = Publicacio.objects.filter(usuari = perfil)
    context = {'perfil':perfil, 'publicacions':publicacions}
    return render(request, 'perfil.html', context)

#FER PETICIO D'AMISTAT
@login_required
def afegirAmic(request, idPerfil):
    jo = request.user.perfil
    amic = get_object_or_404(Perfil, pk=idPerfil)
    
    amics = Amic()
    amics.acceptat = False
    amics.usuari = jo
    amics.usuariAmic = amic
    amics.dataAcceptacio = datetime.date.today()
    amics.save()
    
    tornar = reverse('perfil:perfilAjeno')
    return HttpResponseRedirect(tornar)