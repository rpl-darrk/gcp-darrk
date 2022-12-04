from django import forms
from reservasi_sarana.models import Detail_Pembayaran
from django.contrib.auth.models import User

class UploadBuktiPembayaranForm(forms.ModelForm):
    class Meta:
        model = Detail_Pembayaran
        fields = ['bukti_pembayaran']