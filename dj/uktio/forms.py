from django import forms


class RegionForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial="")
    name = forms.CharField(label="Название региона")
    
    
class OrganizationForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial="")
    name = forms.CharField(label='Название организации')
    city = forms.CharField(label='Город')
    address = forms.CharField(label='Адрес')
    telefone = forms.CharField(label='Телефон', required=False)
    region = forms.ChoiceField(choices=[],label="Регион")
    subordinate = forms.ChoiceField(choices=[], required=False, 
                                    label="Подчиняется")
    