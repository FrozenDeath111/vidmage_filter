from django import forms


class Iud_form(forms.Form):
    files = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))


class CBG_form(forms.Form):
    files = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    files_bg = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))