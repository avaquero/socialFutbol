# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from perfils.models import Perfil, Solicitud
from xarxa.models import Publicacio, Comentari
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import datetime
from django.db.models import Q
from xarxa.forms import FormNovaPublicacio
import datetime
from django.utils import timezone

# Create your views here.
#GENERAR EL TEU PERFIL
def generarPerfil(request):
    perfil = request.user.perfil
    
    if request.method == 'POST':
        form = FormNovaPublicacio(request.POST, request.FILES)
        if form.is_valid():      
            publicacio=form.save(commit=False)
            publicacio.usuari = perfil
            publicacio.save()
            pagina = reverse('perfil:tu')
            return HttpResponseRedirect(pagina)
        else:
            messages.error(request, "Ep! Hi ha hagut un error al introduir un llibre")
    else:
        form = FormNovaPublicacio()
    
    camps_bootstrap = ('text', 'imatge', 'privat')
    for c in camps_bootstrap:
        form.fields[c].widget.attrs['class'] = 'form-control'
    
    
    publicacions = Publicacio.objects.filter(usuari = perfil).order_by('-dataHora')
    peticions = Solicitud.objects.filter(usuariDestinatari = perfil, acceptat = 0)
    nom = []
    idPeticio = []
    amigos = []
    ids = []
    
    for peticio in peticions:
        user_act = Perfil.objects.get(usuari = peticio.usuariSolicitant_id)
        #emmagatzemar en una llista / array
        nom.append(user_act.nom + " " + user_act.cognoms)
        idPeticio.append(peticio.id)
        idPeticio.reverse() #Ordenar la llista al reves per despres fer el pop al template i treurels ordenats
    
    amics = Solicitud.objects.filter(
                                     Q(usuariSolicitant_id = perfil) | Q(usuariDestinatari_id = perfil),
                                     Q(acceptat=True)
                                     )
    
    for amic in amics:
        if amic.usuariSolicitant_id == perfil.id:
            user_act = Perfil.objects.get(usuari = amic.usuariDestinatari_id)
        else:
            user_act = Perfil.objects.get(usuari = amic.usuariSolicitant_id)
        amigos.append(user_act.nom + " " + user_act.cognoms)
        ids.append(user_act.id)
        ids.reverse()
        
    context = {'perfil':perfil, 'publicacions':publicacions, 'nom':nom, 'idPeticio':idPeticio, 'peticions':peticions, 'amigos':amigos, 'ids':ids, 'form':form }
    return render(request, 'tu.html', context)

#GENERAR PERFIL D'aLTRES
def veurePerfil(request, idPerfil):
    perfil = get_object_or_404(Perfil, pk=idPerfil)
    publicacions = Publicacio.objects.filter(usuari = perfil)

    context = {'perfil':perfil, 'publicacions':publicacions }
        
    return render(request, 'perfil.html', context)

#FER PETICIO D'AMISTAT
@login_required
def afegirAmic(request, idPerfil):
    jo = request.user.perfil
    amic = get_object_or_404(Perfil, pk=idPerfil)
    
    amics = Solicitud()
    amics.acceptat = False
    amics.usuariSolicitant = jo
    amics.usuariDestinatari = amic
    amics.dataAcceptacio = datetime.date.today()
    amics.dataSolicitud = datetime.date.today()
    amics.save()
    
    pagina = reverse('perfil:perfilAjeno', kwargs={'idPerfil':idPerfil})
    return HttpResponseRedirect(pagina)

@login_required
def acceptarAmic(request, idLinea):
    Solicitud.objects.filter(id = idLinea).update(acceptat=True)
    pagina = reverse('perfil:tu')
    return HttpResponseRedirect(pagina)
    