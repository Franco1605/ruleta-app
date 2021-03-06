from django.db import models
from django.db.models.fields import DateTimeField
from django_random_id_model import RandomIDModel

# Create your models here.
class Player(RandomIDModel):
    id = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=255)
    dinero = models.PositiveIntegerField(default=10000)

class Round(models.Model):
    fecha = DateTimeField()
    color_ronda = models.CharField(max_length=255)
    jugadores = models.JSONField()