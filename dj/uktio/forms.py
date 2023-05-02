from django import forms


class RegionForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial="")
    name = forms.CharField(label="Название региона")