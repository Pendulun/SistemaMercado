from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('add/', views.CadastroFornecedorView.as_view(), name="supplierregistry"),
    path('add/addsupplier/', views.savesupplier, name="savenewsupplier"),
    path('delete/<int:pk>', views.DeletarFornecedorView.as_view(), name='delete'),
]