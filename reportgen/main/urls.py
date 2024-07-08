from django.urls import path
from . import views

urlpatterns = [
    path("",views.get_data_from_form,name='get_data_from_form')
]