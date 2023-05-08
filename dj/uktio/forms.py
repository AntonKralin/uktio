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
    

class WorkerForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial="")
    name = forms.CharField(label="Имя")
    surname = forms.CharField(label="Фамилия")
    job = forms.CharField(label="Должность")
    organization = forms.ChoiceField(choices=[], required=True,
                                     label="Организация")
    

class CabinetForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial="")
    name = forms.CharField(label="Название")
    description = forms.CharField(label="Описание")
    organization = forms.ChoiceField(choices=[], required=True,
                                     label="Организация")
    