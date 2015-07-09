from django import forms
from geoposition.forms import GeopositionField
from datetime import date
from django.contrib.admin import widgets
from models import Activity
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from datetime import datetime

class ActivityForm(forms.ModelForm):
    activity_date = forms.DateTimeField(label='Fecha de la actividad',
        required=False,
        widget=DateTimePicker(options={"format": "DD-MM-YYYY HH:mm",
                                       "pickSeconds": True, "startDate" :datetime.now().__str__()}))
    
    title = forms.CharField(label='Titulo')
    description = forms.CharField(label='Descripcion', 
                        widget=forms.Textarea(attrs={'placeholder': 'Descripcion, usa hastags para hacer tu plan mas visible a los usuarios...'}))    
    place_name = forms.CharField(label='Nombre del lugar')  
    price = forms.IntegerField(label='Precio')
    limit_participants = forms.IntegerField(label='Limite de participantes')
     
    class Meta:
        model = Activity
        fields = ['title','description', 'activity_date', 'place_name', 'position', 'price', 'limit_participants']
