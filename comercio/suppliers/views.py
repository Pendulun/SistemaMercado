from django.http import HttpResponse, HttpResponseRedirect
from django.urls import  reverse_lazy, reverse
from django.views import generic
from .models import Supplier
from products.models import Product
from django.template import loader


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'suppliers/index.html'
    context_object_name = "suppliers_list"

    def get_queryset(request):
        return Supplier.objects.all()

class SearchView(generic.ListView):
    template_name = 'suppliers/search.html'
    context_object_name = "suppliers_list"

    def get_queryset(self):
        return Supplier.objects.filter(name__icontains = self.request.GET['name']).values()

class CadastroFornecedorView(generic.CreateView):
    template_name_suffix = '_create_form'
    model = Supplier
    fields = ['name','telephone','cnpj','address']

class DeletarFornecedorView(generic.DeleteView):
    model = Supplier
    success_url = reverse_lazy('suppliers:index')

class AtualizarFornecedorView(generic.UpdateView):
    model = Supplier
    fields = ['name','cnpj','telephone','address']
    template_name_suffix = '_update_form'

    success_url = reverse_lazy('suppliers:index')

def product_to_supplier(request):
    template = loader.get_template("suppliers/productToSupplier.html")
    myproducts = Product.objects.all()#[:3]

    supId = request.GET['supplierId']

    supplier = Supplier.objects.get(pk=supId)

    supProducts = supplier.products.all()

    productsToShow = []

    for product in myproducts:
        if product not in supProducts:
            productsToShow.append(product)

    print(f"Products to Show: {productsToShow}")

    context = {
        "myproducts": productsToShow,
        "supplierId": supId
    }

    return HttpResponse(template.render(context, request))

def register_products_to_supplier(request):
    checkboxArgs = [arg for arg in list(request.POST.keys()) if arg[:8] == 'checked-'] 
    mySup = Supplier.objects.get(pk=request.POST['supId'])
    for checkboxName in checkboxArgs:
        checkBoxValue = request.POST[checkboxName]
        mySup.products.add(Product.objects.get(pk=checkBoxValue))

    return HttpResponseRedirect(reverse('suppliers:index'))