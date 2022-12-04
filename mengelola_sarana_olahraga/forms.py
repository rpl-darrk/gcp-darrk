from django import forms
from .models import Sarana


class SaranaForm(forms.ModelForm):
    class Meta:
        model = Sarana
        fields = ('nama', 'url_foto', 'jenis', 'deskripsi')

        widgets = {
            'nama': forms.TextInput(
                attrs={'placeholder': 'Nama Sarana', 'style': 'width: 300px;', 'class': 'form-control'}
            ),
            'url_foto': forms.TextInput(
                attrs={'placeholder': 'URL Foto dari Sarana', 'style': 'width: 300px;', 'class': 'form-control'}
            ),
            'jenis': forms.Select(
                attrs={'placeholder': 'Jenis Sarana', 'style': 'width: 300px;', 'class': 'form-control'}
            ),
            'deskripsi': forms.Textarea(
                attrs={'placeholder': 'Deskripsi dari Sarana', 'style': 'width: 300px;', 'class': 'form-control'}
            )
        }
