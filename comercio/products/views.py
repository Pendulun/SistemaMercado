from json import load
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Product
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def index(request):
    template = loader.get_template("products/index.html")
    myproducts = Product.objects.all().values()

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

def delete(request, id):
  produto = Product.objects.get(id=id)
  produto.delete()
  return HttpResponseRedirect(reverse('products:index'))

def update(request, id):
  myproduct = Product.objects.get(id=id)
  template = loader.get_template('products/update.html')
  context = {
    'myproduct': myproduct,
  }
  return HttpResponse(template.render(context, request))

def updaterecord(request, id):
    nome = request.POST['name']
    marca = request.POST['brand']
    preco = request.POST['price']

    try:
        produto = Product.objects.get(id=id)
        produto.name = nome
        produto.brand = marca
        produto.price = preco

        produto.save()
    except:
        messages.error(request, "Complete corretamente todos os campos de cadastro!")
        return HttpResponseRedirect(reverse("products:update", kwargs={'id':id}))
    else:
    
        return HttpResponseRedirect(reverse('products:index'))

def search(request):
    nome = request.POST['name']
    template = loader.get_template('products/searchProduct.html')

    myproductsearch = Product.objects.filter(name__icontains=nome)

    context = {
        'myproductsearch': myproductsearch,
    }

    return HttpResponse(template.render(context, request))    

def suppliers_of_product(request, pk):
    template = loader.get_template('products/suppliers_of_product.html')
    prodId = pk
    product = Product.objects.get(pk=prodId)

    context = {'product':product}
    return HttpResponse(template.render(context, request))

def buyStock(request):
    prodId = request.POST['prodId']
    supToBuy = 0
    stockToBuy = 0
    try:
        supToBuy = request.POST['supplier']
    except:
        messages.error(request, "Selecione um Fornecedor para comprar")
        return HttpResponseRedirect(reverse("products:suppliers_of_product", kwargs={'pk':prodId}))
    else:
        try:
            stockToBuy = int(request.POST['stockToBuy'])
        except:
            messages.error(request, "Digite apenas números inteiros no estoque!")
            return HttpResponseRedirect(reverse("products:suppliers_of_product", kwargs={'pk':prodId}))
        else:
            product = Product.objects.get(pk=prodId)
            product.stock += stockToBuy
            product.save()
            return HttpResponseRedirect(reverse('products:index')) 