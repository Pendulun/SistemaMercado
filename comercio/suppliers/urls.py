from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('add/', views.CadastroFornecedorView.as_view(), name="supplierregistry"),
    path('delete/<int:pk>', views.DeletarFornecedorView.as_view(), name='delete'),
    path('update/<int:pk>', views.AtualizarFornecedorView.as_view(), name='update'),
]