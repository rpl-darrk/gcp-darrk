from django.urls import path
from . import views

app_name = "mengelola_sarana_olahraga"

urlpatterns = [
    path("", views.index, name="index"),
    path("post_sarana/", views.post_sarana, name="post_sarana"),
    path("update_sarana/<str:id_sarana>", views.update_sarana, name="update_sarana"),
    path("delete_sarana/<str:id_sarana>", views.delete_sarana, name="delete_sarana"),
]
