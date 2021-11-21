import random
import requests
from celery.decorators import task
from datetime import datetime
from celery.utils.log import get_task_logger
from .models import Player, Round
from .aux import definir_apuesta_color
from ruleta.settings import API_KEY


logger = get_task_logger(__name__)

@task
def ruleta():
    ## Hacemos 'girar la ruleta'
    valor_ruleta = random.randint(1,100)
    ## Inicializamos la variable que guardará el color
    color_ruleta = definir_apuesta_color(valor_ruleta)

    ## Hacemos la consulta a la API del clima, que finalmente afecta a la apuesta de los jugadores
    url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q=Santiago&days=3&aqi=no&alerts=no"
    data_weather = requests.get(url).json()
    ## Obtenemos las temperaturas promedio de los dos días siguientes
    temp_dia_1 = data_weather["forecast"]["forecastday"][1]["day"]["avgtemp_c"]
    temp_dia_2 = data_weather["forecast"]["forecastday"][2]["day"]["avgtemp_c"]

    ## Verificamos si alguna temperatura supera los 20°C. De hacerlo, los jugadores se ven afectados
    if temp_dia_1>20 or temp_dia_2>20:
        tipo_apuestas  = "conservadoras"
    else:
        tipo_apuestas = "no conservadoras"

    ##Creamos la lista que tendrá los diccionarios de cada jugador que participa en la ronda, con sus respectivas características
    array_diccionarios_jugadores=[]

    ## Ahora, debemos manejar las apuestas de los jugadores
    jugadores = Player.objects.all()
    for jugador in jugadores:
        ## Creamos el diccionario del jugador
        diccionario_jugador = {}

        ## Hacemos la apuesta del color
        valor_apuesta_jugador = random.randint(1,100)
        color_apostado = definir_apuesta_color(valor_apuesta_jugador)

        ## Revisamos si el jugador tiene saldo. Si no lo tiene, entonces la apuesta es cero
        if jugador.dinero==0:
            apuesta = 0
            porcentaje = 0
            color_apostado = "Ninguno"
        ## Si tiene saldo, hay que verificar si su monto es menor que 1000
        elif jugador.dinero < 1000:
            ## Si es el caso, apuesta todo su dinero (ALL IN)
            porcentaje="No aplica (All in)"
            apuesta = jugador.dinero
            jugador.dinero = 0
        else:
            ## Si no, entonces apostará de acuerdo a un porcentaje:
            ## Si el tipo de apuesta es conservadora, el porcentaje estará entre 3 y 7
            if tipo_apuestas=="conservadoras":
                porcentaje = (random.randint(3,7)/100)
                apuesta = porcentaje * jugador.dinero
                jugador.dinero -= apuesta
            ## Si el tipo de apuesta no es conservadora, el porcentaje estará entre 8 y 15
            else:
                porcentaje = (random.randint(8,15)/100)
                apuesta = porcentaje * jugador.dinero
                jugador.dinero -= apuesta
        
        ## Verificamos el resultado de la apuesta
        if color_ruleta=="VERDE"  and color_apostado==color_ruleta:
            ## Si sale verde y gana, entonces recupera 15 veces lo apostado
            ganancia = 15 * apuesta
            jugador.dinero+=ganancia
            estado = "Ganador"
        elif (color_ruleta=="ROJO" or color_ruleta=="NEGRO") and color_apostado==color_ruleta:
            ## Si sale negro o rojo y gana, entonces recupera el doble de lo apostado
            ganancia = 2 * apuesta
            jugador.dinero+=ganancia
            estado = "Ganador"
        elif color_apostado=="Ninguno":
            estado = "No juega"
            ganancia=0
        else:
            ganancia = 0
            estado = "Perdedor"
        ## Si los colores no coinciden (es decir, el jugador no gana), no se hace más, porque el descuento ya se hace arriba
        ## Completamos el diccionario con la información de la ronda:
        diccionario_jugador["nombre"] = jugador.nombre
        diccionario_jugador["color_apostado"] = color_apostado
        diccionario_jugador["porcentaje_apuesta"] = porcentaje
        diccionario_jugador["apuesta"] = apuesta
        diccionario_jugador["ganancia"] = ganancia
        diccionario_jugador["estado"] = estado
        ## Lo agregamos a la lista
        array_diccionarios_jugadores.append(diccionario_jugador)


        ## Finalmente, guardamos la información en la BDD de jugadores, con los saldos actuales
        jugador.save()

    ## Creamos la instancia de la ronda y la guardamos en la BDD
    ronda = Round(fecha=datetime.now(), color_ronda=color_ruleta, jugadores={"jugadores":array_diccionarios_jugadores})
    ronda.save()

@task
def reponer_dinero():
    jugadores = Player.objects.all()
    ## A todos los jugadores les entregamos 10000
    for jugador in jugadores:
        jugador.dinero+=10000
        jugador.save()