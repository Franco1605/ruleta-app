from django.http.response import ResponseHeaders
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from .models import Player, Round
from .forms import RegistrationForm, EdicionForm
from django.http import HttpResponse

# Create your views here.

## Vista inicial, que contendrá los registros de la ruleta
def home(request):
    context={}
    rondas = Round.objects.all()
    context["rondas"] = rondas
    return render(request, "home.html", context)

## Controlador correspondiente a al index de jugadores
def jugadores(request):
    context = {}
    ## Obtenemos a todos los jugadores desde la BDD
    jugadores = Player.objects.all()
    # Paginamos a los jugadores, de a 5 por página, partiendo en la primera
    p  = Paginator(jugadores, 5)
    page_number = request.GET.get('page', 1)
    try:
        page = p.page(page_number)
    except EmptyPage:
        page = p.page(1)

    # Guardamos a los jugadores en el context y se lo pasamos a la vista del index de jugadores
    context['jugadores'] = page
    return render(request, 'index_jugadores.html', context)

## Controlador que se encarga de crear un jugador nuevo
def registro_jugador(request):
    context={}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jugadores')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm(initial={
            "ultimo_color_apostado":"-",
            "ultimo_dinero_apostado":0,
            "ultimo_dinero_ganado":0,
            "dinero":10000,
        })
        context['registration_form'] = form
    return render(request, "registro_jugador.html", context)

def show_jugador(request, id):
    context={}
    jugador = Player.objects.get(pk=id)
    context['jugador'] = jugador
    return render(request, "show_jugador.html", context)


def edicion_jugador(request, id):
    context={}
    jugador = Player.objects.get(pk=id)
    if request.method == 'POST':
        form = EdicionForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            return redirect(f'/jugadores/{id}/')
        else:
            context['edicion_form'] = form
    else:
        form = EdicionForm(initial={
            "nombre":jugador.nombre,
            "dinero":jugador.dinero,
        })
        context['edicion_form'] = form
    return render(request, "edicion_jugador.html", context)

def eliminar_jugador(request, id):
    Player.objects.filter(id=id).delete()
    return redirect("/jugadores/")
