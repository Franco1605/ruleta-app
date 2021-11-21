from django.urls import include, path
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.home, name='home'),
    path('jugadores/', views.jugadores, name='jugadores'),
    path('registro_jugador/', views.registro_jugador, name='registro_jugador'),
    path('jugadores/<str:id>/', views.show_jugador, name='show_jugador'),
    path('edicion_jugador/<str:id>/', views.edicion_jugador, name='edicion_jugador'),
    path('eliminar_jugador/<str:id>/', views.eliminar_jugador, name='eliminar_jugador'),
]
