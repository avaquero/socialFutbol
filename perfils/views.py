# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from perfils.models import Perfil, Solicitud
from perfils.forms import formulariLogin, formulariModificar, formulariRegistrarse, formulariEditarContrasenya
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from xarxa.models import Publicacio
from django.core import serializers
from django.db.models import Q

#from django.contrib.auth.decorators import login_required

# Create your views here.
def entrar(request):
    #Si el metode es POST es que tenim dades per procesar
    if request.method == 'POST': 
        form = formulariLogin(request.POST)
        #Si les dades entrades són correctes (haurem d'accedir al perfil)
        if form.is_valid():
            #Emmagatzemem les dades que ens envien
            username = form.cleaned_data['usuari']
            password = form.cleaned_data['contrasenya']
            #Autenticar usuaris
            user = authenticate(username=username, password=password)
            #Si es tot correcte
            if user is not None:
                #Pot ser que l'usuari estigui descativat! s'ha de comprovar
                if user.is_active:
                    #Fem login
                    login(request, user)
                    #Si has conseguit fer login aniras a la pagina del teu perfil
                    messages.success(request, 'Login correcte')
                    tu =reverse('home')
                    next = request.GET.get('next', tu)
                    return HttpResponseRedirect(next)
                    # Redirect to a success page.
                else:
                    messages.error(request, 'Compte desactivada, contacti amb l\'administrador')
            # Return a 'disabled account' error message
            else:
                messages.error(request, 'Usuari i/o contrasenya incorrecte')
        # Return an 'invalid login' error message.
            
        else:
            messages.error(request, 'Escriu usuari i contrasenya per accedir')
        #Si no es pots es GET i vol dir que no tenim dades a processar
    else:
        form = formulariLogin() 
        

    #Afegir la clase de bootstrap als camps
    camps_bootestrapejar =( 'usuari', 'contrasenya')
    for c in camps_bootestrapejar:
        form.fields[c].widget.attrs['class'] = 'form-control'
    form.fields['usuari'].widget.attrs['placeholder'] = 'Usuari'
    form.fields['contrasenya'].widget.attrs['placeholder'] = 'Contrasenya'
    
    return render(request, 'login.html', {
        'form': form,
    })
    
def sortir(request):
    logout(request)
    return HttpResponseRedirect('/')

def registrarse(request):
    if request.method == 'POST':
        form = formulariRegistrarse(request.POST, request.FILES)
        if form.is_valid():
            usuari = form.cleaned_data['nick']
            contrasenya = form.cleaned_data['contrasenya']
            nom = form.cleaned_data['nom']
            cognoms = form.cleaned_data['cognoms']
            dataNaix = form.cleaned_data['dataNaix']
            nouUser = User()
            nouUser.username = usuari
            nouUser.set_password(contrasenya)
            nouUser.save()
            
            user = User.objects.get(username = usuari)
            
            nouPerfil = Perfil()
            nouPerfil.usuari = user
            nouPerfil.nom = nom
            nouPerfil.cognoms = cognoms
            nouPerfil.dataNaix = dataNaix
            nouPerfil.equip = "Encara no has introduit equip"
            nouPerfil.save()
            
            messages.success(request, "Molt bé, t'has registrat, ja pots accedir al portal")
            tu = reverse('home')
            return HttpResponseRedirect(tu)
            
        else:
            messages.error(request, "Falten dades per emplenar")
        
       
    else:
        form = formulariRegistrarse()
    
    #Afegir la clase de bootstrap als camps
    camps_bootestrapejar =( 'nick', 'contrasenya', 'nom', 'cognoms', 'dataNaix')
    for c in camps_bootestrapejar:
        form.fields[c].widget.attrs['class'] = 'form-control'
    form.fields['nick'].widget.attrs['placeholder'] = 'Nickname'
    form.fields['contrasenya'].widget.attrs['placeholder'] = 'Contrasenya'
    form.fields['nom'].widget.attrs['placeholder'] = 'Nom'
    form.fields['cognoms'].widget.attrs['placeholder'] = 'Cognoms'
    form.fields['dataNaix'].widget.attrs['placeholder'] = 'Data naixement'
    
    return render(request, 'registrarse.html', {
        'form': form,
    })

@login_required
def modificarDadesPerfil(request):
    perfil = request.user.perfil
    perfil_modificar = get_object_or_404(Perfil, pk=perfil.id)
    
    if request.method == 'POST':
        form = formulariModificar(request.POST, request.FILES, instance = perfil_modificar)
        if form.is_valid():
            form.save()
            pagina = reverse('perfil:tu')
            return HttpResponseRedirect(pagina)
        else:
            messages.error(request, "Hi ha hagut un error")
    else:
        form = formulariModificar(instance = perfil_modificar)
        
    camps_bootstrap = ('nom','cognoms', 'dataNaix', 'equip')
    for c in camps_bootstrap:
        form.fields[c].widget.attrs['class'] = 'form-control'
    return render(request, 'modificarDades.html', {'form':form,})

@login_required
def canviaContrasenya(request):
    if request.method == 'POST':
        form = formulariEditarContrasenya(request.POST)
        if form.is_valid():
            nova = form.cleaned_data['nova']
            novaComprova = form.cleaned_data['novaComprova']
            antiga = form.cleaned_data['antiga']
            usuari = request.user
            if usuari.check_password(antiga):
                if nova != novaComprova:
                    messages.error(request, "Les contrasenyes no corresponen")
                    tu = reverse('accedir:canviPass')
                    return HttpResponseRedirect(tu)
                else:
                    usuari.set_password(nova)
                    usuari.save()
                    messages.success(request, "Contrasenya canviada conrrectament")
                    tu = reverse('perfil:tu')
                    return HttpResponseRedirect(tu)
            else:
                messages.error(request, "La contrasenya actual no es correcte")
    else:
        form = formulariEditarContrasenya()
    
    camps_bootestrapejar =( 'antiga', 'nova', 'novaComprova')
    for c in camps_bootestrapejar:
        form.fields[c].widget.attrs['class'] = 'form-control'
    form.fields['antiga'].widget.attrs['placeholder'] = 'Antiga contrasenya'
    form.fields['nova'].widget.attrs['placeholder'] = 'Contrasenya nova'
    form.fields['novaComprova'].widget.attrs['placeholder'] = 'Repeteix la nova contrasenya'

    return render(request, 'canviContrasenya.html', { 'form': form })

@login_required
def copiaSeguretat(request):
    
    amics = Solicitud.objects.filter(
                                    Q(usuariSolicitant_id = request.user.id) | Q(usuariDestinatari_id = request.user.id),
                                    Q(acceptat = True)
                                    )
    
    copia = list(Perfil.objects.filter(id=request.user.id)) + list(Publicacio.objects.filter(usuari_id = request.user.id)) + list(amics)
    
    data = serializers.serialize('xml', copia)
    
    return HttpResponse(data, content_type="application/xml")