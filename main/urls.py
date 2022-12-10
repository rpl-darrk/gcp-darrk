from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("daftar-gor", views.gor_list, name="gor-list"),
]
