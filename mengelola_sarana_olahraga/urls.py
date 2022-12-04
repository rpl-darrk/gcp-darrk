from django.urls import path

from . import views

app_name = "mengelola_sarana_olahraga"

urlpatterns = [
    path("", views.index, name="index"),
]
