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
    publicacions = Publicacio.objects.filter(usuari = perfil).order_by('-dataHora')
    peticions = Amic.objects.filter(usuariAmic = perfil, acceptat = 0)
    nom = []
    idPeticio = []
    
    for peticio in peticions:
        user_act = Perfil.objects.get(usuari = peticio.usuari_id)
        #emmagatzemar en una llista / array
        nom.append(user_act.nom + " " + user_act.cognoms)
        idPeticio.append(peticio.id)
        idPeticio.reverse() #Ordenar la llista al reves per despres fer el pop al template i treurels ordenats
    
    context = {'perfil':perfil, 'publicacions':publicacions, 'nom':nom, 'idPeticio':idPeticio, 'peticions':peticions }
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