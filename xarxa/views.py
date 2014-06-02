# -*- encoding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
from django.core import serializers

# Create your views here.

#GENERAR EL MEU PERFIL
def generarPerfil(request):
    
    if not request.user.is_authenticated():
        pagina = reverse('accedir:login')
        messages.error(request, "Encara no has iniciat sessio")
        return HttpResponseRedirect(pagina)
    else:
        perfil = request.user.perfil

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
            com = FormNouComentari()
        
        com.fields['comentari'].widget.attrs['class'] = 'form-control'
        
        ## Aqui es crea el formulari per obtenir el modal, amb aquest formulari que crea les publicacions
        if request.method == 'POST':
            form = FormNovaPublicacio(request.POST, request.FILES)
            if form.is_valid():      
                publicacio=form.save(commit=False)
                publicacio.usuari = perfil
                publicacio.save()
                pagina = reverse('perfil:tu')
                return HttpResponseRedirect(pagina)
            else:
                messages.error(request, "ERROR! No s'ha pogut crear la publicació perque no has indtoduït cap dada")
                pagina = reverse('perfil:tu')
                return HttpResponseRedirect(pagina)
        else:
            form = FormNovaPublicacio()
        
        camps_bootstrap = ('text','url', 'privat')
        for c in camps_bootstrap:
            form.fields[c].widget.attrs['class'] = 'form-control'
        
        
        publicacio = Publicacio.objects.filter(usuari = perfil).order_by('-dataHora')
        paginator = Paginator(publicacio, 10)
        page = request.GET.get('pagina')
        try:
            publicacions = paginator.page(page)
        except PageNotAnInteger:
            publicacions = paginator.page(1)
        except EmptyPage:
            publicacions = paginator.page(1)
        
        
        peticion = Solicitud.objects.filter(
                                         Q(usuariSolicitant_id = perfil) | Q(usuariDestinatari_id = perfil),
                                         Q(acceptat=False)
                                         )
        
        peticions = Perfil.objects.filter( id__in =  [x.usuariSolicitant_id for x in peticion] + [x.usuariDestinatari_id for x in peticion] ).exclude(id = request.user.perfil.id)

        idPeticio = []
       
        for pet in peticion:
            idPeticio.append(pet.id)
        idPeticio.reverse() #Ordenar la llista al reves per despres fer el pop al template i treurels ordenats
        
        amics = Solicitud.objects.filter(
                                         Q(usuariSolicitant_id = perfil) | Q(usuariDestinatari_id = perfil),
                                         Q(acceptat=True)
                                         )
        
        
        amigos = Perfil.objects.filter( id__in =  [x.usuariSolicitant_id for x in amics] + [x.usuariDestinatari_id for x in amics] ).exclude(id = request.user.perfil.id)
        
          

        context = {'perfil':perfil, 'publicacions':publicacions, 'peticions':peticions, 'amigos':amigos, 'form':form, 'com':com, 'idPeticio':idPeticio }
        return render(request, 'tu.html', context)

#GENERAR PERFIL D'aLTRES
def veurePerfil(request, idPerfil):
    if request.user.is_authenticated() and int(idPerfil) == request.user.perfil.id:
        pagina = reverse('perfil:tu')
        return HttpResponseRedirect(pagina)

    else:
        perfil = get_object_or_404(Perfil, pk=idPerfil)
        
        publicacio = Publicacio.objects.filter(usuari = idPerfil).order_by('-dataHora')
        
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
            else:
                publicacio = Publicacio.objects.filter(usuari = idPerfil).order_by('-dataHora').exclude(privat = True)
            
            if pendent == True:
                publicacio = Publicacio.objects.filter(usuari = idPerfil).order_by('-dataHora').exclude(privat = True)
    
        else:
            publicacio = Publicacio.objects.filter(usuari = idPerfil).order_by('-dataHora').exclude(privat = True)
    
            
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
        
        paginator = Paginator(publicacio, 10)
        page = request.GET.get('pagina')
        try:
            publicacions = paginator.page(page)
        except PageNotAnInteger:
            publicacions = paginator.page(1)
        except EmptyPage:
            publicacions = paginator.page(1)
                
        form.fields['comentari'].widget.attrs['class'] = 'form-control'
        
        context = {'perfil':perfil, 'publicacions':publicacions, 'amics':amics, 'pendent':pendent, 'form':form, 'linea':linea, 'idPerfil':idPerfil }
    
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
                             
    messages.success(request, "Amic acceptat")
    pagina = reverse('perfil:tu')
    return HttpResponseRedirect(pagina)

@login_required
def eliminarSolicitud(request, idLinea):
    Solicitud.objects.filter(
                             Q(usuariSolicitant_id = request.user.perfil.id) | Q(usuariDestinatari_id = request.user.perfil.id),
                             Q(id = idLinea)
                             ).delete()
    
    messages.success(request, "Solicitud denegada")
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
        
    camps_bootstrap = ('text','url', 'privat')
    for c in camps_bootstrap:
        form.fields[c].widget.attrs['class'] = 'form-control'
    return render(request, 'modificarPublicacio.html', {'form':form,})

@login_required
def eliminaPublicacio(request, idPublicacio):
    perfil = request.user.perfil
    Publicacio.objects.filter(pk = idPublicacio, usuari = perfil).delete()
    
    messages.success(request, "Publicació eliminada")
    pagina = reverse('perfil:tu')
    return HttpResponseRedirect(pagina)

def recerca(request):
    if request.method == 'POST':
        form = BuscaForm(request.POST)
        if form.is_valid():
            buscat = form.cleaned_data['busca']
            
            url_next = reverse('recerca')
            return HttpResponseRedirect( url_next + "?q=" + buscat)
        else:
            messages.error(request, "No has introduit res a la cerca")
            return HttpResponseRedirect('/')
        
    else:    
        form = BuscaForm()   
        buscat = request.GET.get("q", '')
        perfils = Perfil.objects.filter(nom__contains= buscat)
    return render(request, 'recerca.html', { 'formCerca': form, 'perfils':perfils })

# Funcio per buscar perfils a la barra
def perfils(request):
    cadena = request.GET.get('cadena','')

    nom = Q(nom__contains = cadena)
    cognom = Q(cognoms__contains = cadena)
    perfils = Perfil.objects.filter(nom | cognom) if cadena else Perfil.objects.none()
    
    perfilsJson = serializers.serialize('json', perfils)
    
    return HttpResponse(perfilsJson, content_type="application/json")

def perfilAltreAjax(request):
    
    numPub = request.GET['max']
    idPerfil = request.GET['idPerfil']
    perfil = get_object_or_404(Perfil, pk=idPerfil)
    
    
    publicacions = Publicacio.objects.filter(usuari = perfil).order_by('-dataHora')[:numPub]
    
    amics = False
    pendent = False
    
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
    
        #A partir d'aqui si no som amics no mostro les publis privades, i si la solicitud es pendent tampoco mostro les privades
        else:
            publicacions = Publicacio.objects.filter(usuari = idPerfil).order_by('-dataHora').exclude(privat = True)[:numPub]
        
        if pendent == True:
            publicacions = Publicacio.objects.filter(usuari = idPerfil).order_by('-dataHora').exclude(privat = True)[:numPub]
    else:
        publicacions = Publicacio.objects.filter(usuari = idPerfil).order_by('-dataHora').exclude(privat = True)[:numPub]
    
       
    
    publicacionsJson = serializers.serialize('json', publicacions )
  
    return HttpResponse(publicacionsJson, content_type="application/json")

def comentarisAjax(request):
    comentaris = Comentari.objects.all()
    comentarisJson = serializers.serialize('json', comentaris )
  
    return HttpResponse(comentarisJson, content_type="application/json")

def perfilAjax(request):
    perfils = Perfil.objects.all()
    perfilsJson = serializers.serialize('json', perfils )
  
    return HttpResponse(perfilsJson, content_type="application/json")

@login_required
def perfilTuAjax(request):
    numPub = request.GET['max']
    perfil = request.user.perfil
    
    publicacions = Publicacio.objects.filter(usuari = perfil).order_by('-dataHora')[:numPub]
    
    publicacionsJson = serializers.serialize('json', publicacions )
  
    return HttpResponse(publicacionsJson, content_type="application/json")

def compartirPub(request, idPub):
    publicacio = get_object_or_404(Publicacio, pk = idPub)
    if request.method == 'GET':
        form = FormNouComentari(request.GET)
        if form.is_valid():      
            comentari=form.save(commit=False)
            comentari.publicacio_id = request.GET['publicacio']
            comentari.usuari = request.user.perfil
            comentari.save()
            pagina = reverse('perfil:compartirPub', kwargs={'idPub':idPub})
            return HttpResponseRedirect(pagina)
    else:
        form = FormNouComentari()
        
    
    form.fields['comentari'].widget.attrs['class'] = 'form-control'
    context = {'publicacio':publicacio, 'form':form}
    return render(request, 'compartirPubicacio.html', context)
    
    