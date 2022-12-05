from django.urls import path
from ..view import views_mengelola_sarana

app_name = "mengelola_sarana_olahraga"

urlpatterns = [
    path("", views_mengelola_sarana.index, name="index"),
    path("post_sarana/", views_mengelola_sarana.post_sarana, name="post_sarana"),
    path("update_sarana/<str:id_sarana>",
         views_mengelola_sarana.update_sarana, name="update_sarana"),
    path("delete_sarana/<str:id_sarana>",
         views_mengelola_sarana.delete_sarana, name="delete_sarana"),
]
