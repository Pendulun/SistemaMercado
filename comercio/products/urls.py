from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name="index"),
    path('add/', views.add, name="productregistry"),
    path('add/addproduct/', views.saveproduct, name="savenewproduct"),
]