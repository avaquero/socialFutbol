from xarxa.forms import BuscaForm

#Context procesor de la barra de recerca
def formulariCerca(request):
    return {'formCerca':BuscaForm() }