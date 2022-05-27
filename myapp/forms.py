from django import forms
from django.forms import ModelForm
from .models import StudentName
class CreateNewList(forms.Form):
    name = forms.CharField(label="Name",max_length=20,required=True)


class studentRegistration(ModelForm):
    class Meta:
        model = StudentName
        fields = ['name','fname','gender','address','entry','image']

