from django import forms
from .models import *
from django.contrib.auth.models import User


class UploadBuktiPembayaranForm(forms.ModelForm):
    class Meta:
        model = Detail_Pembayaran
        fields = ['bukti_pembayaran']
