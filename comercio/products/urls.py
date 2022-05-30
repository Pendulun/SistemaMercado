from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name="index"),
    path('add/', views.add, name="productregistry"),
    path('add/addproduct/', views.saveproduct, name="savenewproduct"),
    path('delete/<int:id>', views.delete, name='delete'),
    path('update/<int:id>', views.update, name='update'),
    path('update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
    path('search/', views.search, name="searchproduct"),
    path('suppliersOfProduct/<int:pk>', views.suppliers_of_product, name='suppliers_of_product'),
    path('buyStock/', views.buyStock, name='buyStock'),
]