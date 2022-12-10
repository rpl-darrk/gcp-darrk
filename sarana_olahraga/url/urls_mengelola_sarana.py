from django.urls import path
from ..view import views_mengelola_sarana

app_name = "mengelola_sarana_olahraga"

urlpatterns = [
    path("", views_mengelola_sarana.index, name="index"),
    path("add-sarana/", views_mengelola_sarana.add_sarana, name="add-sarana"),
    path("update-sarana/<str:id_sarana>",
         views_mengelola_sarana.update_sarana, name="update-sarana"),
    path("delete-sarana/<str:id_sarana>",
         views_mengelola_sarana.delete_sarana, name="delete-sarana"),
]
