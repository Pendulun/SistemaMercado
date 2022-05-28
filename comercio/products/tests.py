from django.test import TestCase
from .models import Product
from django.urls import reverse

# Create your tests here.
class ProductIndexViewTests(TestCase):
    def test_no_products(self):
        """
        Testa se aparece uma mensagem de erro apropriada quando não houverem produtos cadastrados
        """
        response = self.client.get(reverse("products:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não existem produtos cadastrados.")
        self.assertQuerysetEqual(response.context['myproducts'], [])

    def test_add_one_product(self):
        """
        Testa se o produto recém cadastrado é enviado para a página de index
        """
        prodName = "Chocolate"
        prodPrice = 4.5
        prodBrand = 'Lacta'
        prodStock = 0
        prodSold = 0

        novoproduto = Product.objects.create(name=prodName, price=prodPrice,
                                             brand=prodBrand, stock=prodStock, sold=prodSold)

        response = self.client.get(reverse("products:index"))
        self.assertEqual(response.status_code, 200)

        prodDict = {
            'name':prodName,
            'price':prodPrice,
            'brand':prodBrand,
            'stock':prodStock,
            'sold':prodSold,
            'id':1
        }

        self.assertEqual(response.context['myproducts'][0], prodDict)

class ProductRegisterViewTests(TestCase):
    def test_register_product(self):
        """
        Testa se o produto cadastrado na tela de cadastro é enviado para o index
        """
        prodName = "Chocolate"
        prodPrice = 4.5
        prodBrand = 'Lacta'

        postData = {
            'name':prodName,
            'price':prodPrice,
            'brand':prodBrand
        }

        response = self.client.post(reverse("products:savenewproduct"), data = postData, follow=True)
        self.assertEqual(response.status_code, 200)

        prodDict = {
            'name':prodName,
            'price':prodPrice,
            'brand':prodBrand,
            'stock':0,
            'sold':0,
            'id':1
        }

        self.assertEqual(response.context['myproducts'][0], prodDict)
    
    def test_register_product_with_no_info(self):
        """
        Testa se uma mensagem de erro aparece caso seja feito um cadastro com valores inválidos
        """
        prodName = "Chocolate"
        prodPrice = ''
        prodBrand = 'Lacta'

        postData = {
            'name':prodName,
            'price':prodPrice,
            'brand':prodBrand
        }

        response = self.client.post(reverse("products:savenewproduct"), data = postData, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Complete corretamente todos os campos de cadastro!")
