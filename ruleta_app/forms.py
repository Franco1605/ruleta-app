from django import forms
from .models import Player



class RegistrationForm(forms.ModelForm):
    
    nombre = forms.CharField(max_length=254, label='Ingrese el nombre del jugador', widget=forms.TextInput(attrs={
        'placeholder': 'Nombre del jugador',
    }))

    dinero = forms.IntegerField(label="Ingrese el monto de dinero inicial del jugador", widget=forms.NumberInput(attrs={
        'placeholder': 'Monto inicial',
    }))
    
    class Meta:
        model = Player
        fields = ("nombre", "dinero")

class EdicionForm(forms.ModelForm):
    
    nombre = forms.CharField(max_length=254, label='Ingrese el nuevo nombre del jugador', widget=forms.TextInput(attrs={
        'placeholder': 'Nombre del jugador',
    }))

    dinero = forms.IntegerField(label="Ingrese el nuevo monto de dinero inicial del jugador", widget=forms.NumberInput(attrs={
        'placeholder': 'Monto inicial',
    }))
    
    class Meta:
        model = Player
        fields = ("nombre", "dinero")