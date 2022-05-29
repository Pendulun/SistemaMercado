from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Supplier
from django.contrib import messages


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'suppliers/index.html'
    context_object_name = "suppliers_list"

    def get_queryset(request):
        return Supplier.objects.all()


class CadastroFornecedorView(generic.CreateView):
    template_name_suffix = '_create_form'
    model = Supplier
    fields = ['name','telephone','cnpj','address']

def savesupplier(request):
    nome = request.POST['name']
    phone = request.POST['telephone']
    cnpj = request.POST['cnpj']
    endereco = request.POST['address']
    try:
        novoSupplier = Supplier(name=nome, telephone=phone, cnpj=cnpj, address=endereco)
        novoSupplier.save()
    except:
        messages.error(request, "Complete corretamente todos os campos de cadastro!")
        return HttpResponseRedirect(reverse("suppliers:supplierregistry"))
    else:
        return HttpResponseRedirect(reverse("suppliers:index"))
