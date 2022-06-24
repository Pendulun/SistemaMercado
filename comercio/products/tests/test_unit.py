from django.test import TestCase
from ..models import Product
from django.urls import reverse

class ProductIndexViewTests(TestCase):
    def test_index_no_products_warning_message(self):
        """
        Testa se aparece uma mensagem de erro apropriada quando não houverem produtos cadastrados
        """
        response = self.client.get(reverse("products:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não existem produtos cadastrados.")
        self.assertQuerysetEqual(response.context['myproducts'], [])

    def test_new_product_sent_to_index(self):
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

        novoproduto.delete()

class ProductRegisterViewTests(TestCase):
    def test_registered_product_sent_to_index(self):
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
    
    def test_cant_register_product_invalid_info(self):
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
    
class ProductSearchViewTests(TestCase):
    
    def test_cant_find_unregistered_product(self):
        searchedProdName = "Chocolate"

        postData = {'name':searchedProdName}
        response = self.client.post(reverse("products:searchproduct"), data = postData, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['myproductsearch'], [])
    
    def test_can_find_registered_product_by_complete_name(self):
        prodName = "Chocolate"
        prodPrice = 4.5
        prodBrand = 'Lacta'
        prodStock = 0
        prodSold = 0
        
        productList = [{   'name': prodName,
                            'price': prodPrice,
                            'brand': prodBrand,
                            'stock': prodStock,
                            'sold': prodSold
                        }]
        
        novoProduto = self.create_products_and_return(productList)[0]

        postData = {'name' : prodName}
        response = self.client.post(reverse("products:searchproduct"), data = postData, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['myproductsearch'], [novoProduto])
        
        novoProduto.delete()

    def test_can_find_registered_product_by_incomplete_name(self):
        prodName = "Chocolate"
        prodPrice = 4.5
        prodBrand = 'Lacta'
        prodStock = 0
        prodSold = 0

        productList = [{   'name': prodName,
                            'price': prodPrice,
                            'brand': prodBrand,
                            'stock': prodStock,
                            'sold': prodSold
                        }]

        novoProduto = self.create_products_and_return(productList)[0]

        NUM_CHARS_FOR_QUERY = 5
        postData = {'name' : prodName[:NUM_CHARS_FOR_QUERY]}
        response = self.client.post(reverse("products:searchproduct"), data = postData, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['myproductsearch'], [novoProduto])
        
        novoProduto.delete()
    
    def test_can_find_multiple_products_by_incomplete_name(self):
        prodPrice = 4.5
        prodBrand = 'Lacta'
        prodStock = 0
        prodSold = 0

        prodNames = ["Chocolate", "Barra de Chocolate"]

        productList = [{   'name': prodName,
                            'price': prodPrice,
                            'brand': prodBrand,
                            'stock': prodStock,
                            'sold': prodSold
                        } for prodName in prodNames]
        
        produtosCriados = self.create_products_and_return(productList)


        NUM_CHARS_FOR_QUERY = 5
        postData = {'name' : 'Chocolate'[:NUM_CHARS_FOR_QUERY]}
        response = self.client.post(reverse("products:searchproduct"), data = postData, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['myproductsearch'], produtosCriados, ordered=False)
        
        [produto.delete() for produto in produtosCriados]
    
    def test_dont_get_uncorrelated_products_by_incomplete_name(self):
        prodPrice = 4.5
        prodBrand = 'Lacta'
        prodStock = 0
        prodSold = 0

        prodNames = ["Chocolate", "Barra de Chocolate", "Espaguete"]

        productList = [{   'name': prodName,
                            'price': prodPrice,
                            'brand': prodBrand,
                            'stock': prodStock,
                            'sold': prodSold
                        } for prodName in prodNames]
        
        produtosCriados = self.create_products_and_return(productList)
        
        NUM_CHARS_FOR_QUERY = 5
        post_data = {'name' : 'Chocolate'[:NUM_CHARS_FOR_QUERY]}
        response = self.client.post(reverse("products:searchproduct"), data = post_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['myproductsearch'], produtosCriados[:2], ordered=False)
        
        [produto.delete() for produto in produtosCriados]
    
    def create_products_and_return(self, productsList):

        createdProductsList = [
                                    Product.objects.create( name=product['name'],
                                                            price=product['price'],
                                                            brand=product['brand'],
                                                            stock=product['stock'],
                                                            sold=product['sold'] )
                                    for product in productsList
                                ]

        return createdProductsList

class ProductBuyProductViewTest(TestCase):
    def setUp(self):
        self.novoProduto = Product.objects.create( name='Chocolate', price=4.2,
                                brand='Lacta', stock= 15,
                                sold=0)
    
    def tearDown(self):
        self.novoProduto.delete()

    def test_can_buy_product(self):
        post_data = {'quantidade' : 5}
        response = self.client.post(reverse("products:buyProduct", kwargs={'id':self.novoProduto.id}), data = post_data, follow=True)
        
        self.assertEqual(response.status_code, 200)

        self.novoProduto.stock -= post_data['quantidade']
        self.novoProduto.sold += post_data['quantidade']

        self.assertEqual(response.context['myproduct'], self.novoProduto)
    
    def test_cant_buy_if_quantity_bigger_than_stock(self):
        post_data = {'quantidade' : 30}
        response = self.client.post(reverse("products:buyProduct", kwargs={'id':self.novoProduto.id}), data = post_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['myproduct'], self.novoProduto)
    
    def test_cant_buy_negative_quantity(self):
        post_data = {'quantidade' : -1}
        response = self.client.post(reverse("products:buyProduct", kwargs={'id':self.novoProduto.id}), data = post_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['myproduct'], self.novoProduto)

    def test_cant_buy_non_int_quantity(self):
        post_data = {'quantidade' : 'test'}
        response = self.client.post(reverse("products:buyProduct", kwargs={'id':self.novoProduto.id}), data = post_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['myproduct'], self.novoProduto)