from django import forms
from .models import *

class profil_P_form(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('img_patient','nomPatient',
        'prenomPatient','date_naiss','blood',
        'genre','telephone','Address', 'commune',
        'wilaya')

class profil_D_form(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = '__all__'
        
class Motif_form(forms.ModelForm):
    class Meta:
        model = type_consultation
        fields = '__all__'
        
class specialiteForm(forms.ModelForm):
    class Meta:
        model = specialite
        fields = '__all__'