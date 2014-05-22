# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from perfils.models import Perfil, Solicitud
from xarxa.models import Publicacio, Comentari
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from xarxa.forms import FormNovaPublicacio, FormNouComentari, BuscaForm
import datetime
from django.utils import timezone
from django.utils import simplejson
import json
from django.core import serializers

# Create your views here.

#GENERAR EL TEU PERFIL
def generarPerfil(request):
    perfil = request.user.perfil

    ## Formulari per crear comentaris
    #Crear formulari per comentar publicacions
    if request.method == 'GET':
        com = FormNouComentari(request.GET)
        if com.is_valid():      
            comentari=com.save(commit=False)
            comentari.publicacio_id = request.GET['publicacio']
            comentari.usuari = request.user.perfil
            comentari.save()
            pagina = reverse('perfil:tu')
            return HttpResponseRedirect(pagina)
    else:
        form = FormNouComentari()
    
    
    ## Aqui es crea el formulari per obtenir el modal, amb aquest formulari
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
    
    camps_bootstrap = ('text', 'privat')
    for c in camps_bootstrap:
        form.fields[c].widget.attrs['class'] = 'form-control'
    
    comentaris = Comentari.objects.all()
    publicacions = Publicacio.objects.filter(usuari = perfil).order_by('-dataHora')
    peticions = Solicitud.objects.filter(usuariDestinatari = perfil, acceptat = 0)
    nom = []
    idPeticio = []
    amigos = []
    ids = []
    
    #variable per poder fer link al perfil que et fa la peticio
    link = ""
    
    for peticio in peticions:
        user_act = Perfil.objects.get(usuari = peticio.usuariSolicitant_id)
        #emmagatzemar en una llista / array
        nom.append(user_act.nom + " " + user_act.cognoms)
        link = user_act.id
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
        
    context = {'perfil':perfil, 'publicacions':publicacions, 'nom':nom, 'idPeticio':idPeticio, 'peticions':peticions, 'amigos':amigos, 'ids':ids, 'form':form, 'comentaris':comentaris, 'com':com, 'link':link }
    return render(request, 'tu.html', context)

#GENERAR PERFIL D'aLTRES
def veurePerfil(request, idPerfil):
    perfil = get_object_or_404(Perfil, pk=idPerfil)
    
    publicacions = Publicacio.objects.filter(usuari = perfil).order_by('-dataHora')
    comentaris = Comentari.objects.all()
    
    amics = False
    pendent = False
    linea = ""
    
    #Comprovo que l'usuari si esta autenticat si es aixi, miro si soc amic del perfil que visito
    if request.user.is_authenticated():
        yo = request.user.perfil
        amics = Solicitud.objects.filter(
                                         Q(usuariSolicitant_id = idPerfil) | Q(usuariDestinatari_id = idPerfil),
                                         Q(usuariSolicitant_id = yo.id) | Q(usuariDestinatari_id = yo.id)
                                         ).exists()
        #si existeix un registre miro si som amics, o esta pendent la solicitud
        if amics:
            mirarPendent = Solicitud.objects.filter(
                                         Q(usuariSolicitant_id = idPerfil) | Q(usuariDestinatari_id = idPerfil),
                                         Q(usuariSolicitant_id = yo.id) | Q(usuariDestinatari_id = yo.id)
                                         )
            for x in mirarPendent:
                if x.acceptat:
                    pendent = False
                else:
                    pendent= True
                linea = x.id  
    
    #A partir d'aqui si no som amics no mostro les publis privades, i si la solicitud es pendent tampoco mostro les privades
    if not amics:
        publicacions = publicacions.exclude( privat = True )
    
    if pendent == True:
        publicacions = publicacions.exclude( privat = True )
        
    #Crear formulari per comentar publicacions
    if request.method == 'GET':
        form = FormNouComentari(request.GET)
        if form.is_valid():      
            comentari=form.save(commit=False)
            comentari.publicacio_id = request.GET['publicacio']
            comentari.usuari = request.user.perfil
            comentari.save()
            pagina = reverse('perfil:perfilAjeno', kwargs={'idPerfil':idPerfil})
            return HttpResponseRedirect(pagina)
    else:
        form = FormNouComentari()
    
    #camps_bootstrap = ('comentari')
    #for c in camps_bootstrap:
        #form.fields[c].widget.attrs['class'] = 'form-control'
    
    context = {'perfil':perfil, 'publicacions':publicacions, 'amics':amics, 'pendent':pendent, 'comentaris':comentaris, 'form':form, 'linea':linea }
        
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
    Solicitud.objects.filter(
                             Q(usuariSolicitant_id = request.user.perfil.id) | Q(usuariDestinatari_id = request.user.perfil.id),
                             Q(id = idLinea)
                             ).update(acceptat=True)
    pagina = reverse('perfil:tu')
    return HttpResponseRedirect(pagina)

@login_required
def eliminarSolicitud(request, idLinea):
    Solicitud.objects.filter(
                             Q(usuariSolicitant_id = request.user.perfil.id) | Q(usuariDestinatari_id = request.user.perfil.id),
                             Q(id = idLinea)
                             ).delete()
    
    pagina = reverse('perfil:tu')
    return HttpResponseRedirect(pagina)

@login_required
def modificaPublicacio(request, idPublicacio):
    perfil = request.user.perfil
    publicacio = get_object_or_404(Publicacio, pk = idPublicacio, usuari = perfil)
    
    if request.method == 'POST':
        form = FormNovaPublicacio(request.POST, request.FILES, instance = publicacio)
        if form.is_valid():
            form.save()
            pagina = reverse('perfil:tu')
            return HttpResponseRedirect(pagina)
        else:
            messages.error(request, "Hi ha hagut un error al modificar la publicacio")
    else:
        form = FormNovaPublicacio(instance = publicacio)
        
    camps_bootstrap = ('text', 'privat')
    for c in camps_bootstrap:
        form.fields[c].widget.attrs['class'] = 'form-control'
    return render(request, 'modificarPublicacio.html', {'form':form,})

def recerca(request):
    if request.method == 'POST':
        form = BuscaForm(request.POST)
        if form.is_valid():
            buscat = form.cleaned_data['busca']
            
            url_next = reverse('recerca')
            return HttpResponseRedirect( url_next + "?q=" + buscat)
        else:
            messages.error(request, "Ep! Busqueda no vàlida")
            return HttpResponseRedirect('/')
        
    else:    
        form = BuscaForm()   
        buscat = request.GET.get("q", '')
        perfils = Perfil.objects.filter(nom__contains= buscat)
    return render(request, 'recerca.html', { 'formCerca': form, 'perfils':perfils })

def perfils(request):
    cadena = request.GET['cadena']
    max = request.GET['max']
    nom = Q(nom__contains = cadena)
    cognom = Q(cognoms__contains = cadena)
    perfils = Perfil.objects.filter(nom | cognom)
    
    perfilsJson = serializers.serialize('json', perfils)
    return HttpResponse(perfilsJson, content_type="application/json")
              
    