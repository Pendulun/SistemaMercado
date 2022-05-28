from json import load
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Product
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def index(request):
    template = loader.get_template("products/index.html")
    myproducts = Product.objects.all().values()#[:3]

    context = {
        "myproducts": myproducts,
    }

    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template("products/addProduct.html")
    return HttpResponse(template.render({}, request))

def saveproduct(request):
    nome = request.POST['name']
    preco = request.POST['price']
    marca = request.POST['brand']
    estoque = 0
    vendidos = 0
    try:
        novoProduto = Product(name=nome, price=preco, brand=marca, stock=estoque, sold=vendidos)
        novoProduto.save()
    except:
        messages.error(request, "Complete corretamente todos os campos de cadastro!")
        return HttpResponseRedirect(reverse("products:productregistry"))
    else:
        return HttpResponseRedirect(reverse("products:index"))
