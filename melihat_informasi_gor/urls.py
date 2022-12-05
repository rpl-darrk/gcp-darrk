from django.urls import path
from .views import *

urlpatterns = [
    path('info-gor/<str:ID_gor>', get_info_gor, name='get_info_gor')
]