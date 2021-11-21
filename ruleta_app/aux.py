import random

def definir_apuesta_color(num):
    color_obtenido = ""
    lista_valores_color_rojo = range(3,52)
    lista_valores_color_negro = range(52,101)
    ## Si se obtiene 1 ó 2, el color es VERDE
    if num == 1 or num==2:
        color_obtenido = "VERDE"
    ## Si se obtiene un valor entre 3 y 51, entonces el color de la ruleta es rojo
    elif num in lista_valores_color_rojo:
        color_obtenido = "ROJO"
    ## Si se obtiene un valor entre 52 y 100, entonces el color de la ruleta es negro
    elif num in lista_valores_color_negro:
        color_obtenido = "NEGRO"
        
    return color_obtenido
