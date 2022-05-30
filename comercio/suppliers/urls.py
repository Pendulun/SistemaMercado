from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('add/', views.CadastroFornecedorView.as_view(), name="supplierregistry"),
    path('search/', views.SearchView.as_view(), name='search'),
    path('delete/<int:pk>', views.DeletarFornecedorView.as_view(), name='delete'),
    path('update/<int:pk>', views.AtualizarFornecedorView.as_view(), name='update'),
    path('registerProduct/', views.product_to_supplier_view, name='product_to_supplier'),
    path('registerProducts/', views.register_products_to_supplier, name='register_products_to_supplier'),
    path('unregisterProduct/', views.remove_product_to_supplier_view, name='remove_product_of_supplier'),
    path('unregisterProducts/', views.remove_products_of_supplier, name='unregister_products_to_supplier'),
]