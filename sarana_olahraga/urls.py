from django.urls import path

from . import views

app_name = "sarana_olahraga"

urlpatterns = [
    path("sarana/<str:ID_gor>", views.getSaranaOlaharaga, name="sarana_olahraga"),
]
