from django.test import TestCase
from django.urls import reverse
from products.models import Product
from suppliers.models import Supplier


class ProductAndSupplierIntegrationTests(TestCase):

    def setUp(self):
        self.produto = self.create_base_product()
        self.supplier = self.create_base_supplier()
    
    def create_base_product(self):
        prodName = "Chocolate"
        prodPrice = 4.5
        prodBrand = 'Lacta'
        prodStock = 0
        prodSold = 0
        return Product.objects.create(name=prodName, price=prodPrice,
                                            brand=prodBrand, stock=prodStock, sold=prodSold)
    
    def create_base_supplier(self):
        supName = "Fornecedor Teste"
        supTel = "(31) 12345-6789"
        supCnpj = '1234567890'
        supAddress = "Rua Teste"

        return Supplier.objects.create(name=supName, telephone=supTel,
                                            cnpj=supCnpj, address=supAddress)
    
    def get_associate_post_data_dict(self, supId:int, produtoId:int):
        return {'supId':supId, f'checked-{produtoId}': produtoId}
    
    def get_buy_stock_post_data_dict(self, prodId:int, supId:int, stock_to_buy:int):
        return {'prodId': prodId, 'supplier': supId, 'stockToBuy': stock_to_buy}
    
    def get_buy_product_as_client_post_data_dict(self, amount_to_buy:int):
        return {'quantidade':amount_to_buy}

    def test_can_associate_product_to_supplier(self):

        postData = self.get_associate_post_data_dict(self.supplier.id, self.produto.id) 
        self.client.post(reverse("suppliers:register_products_to_supplier"), data = postData, follow=True)
        self.assertQuerysetEqual(self.supplier.products.all(), [self.produto])
    
    def test_can_buy_stock_for_product_with_supplier(self):
        
        associatePostData = self.get_associate_post_data_dict(self.supplier.id, self.produto.id) 
        self.client.post(reverse("suppliers:register_products_to_supplier"), data = associatePostData, follow=True)

        STOCK_TO_BUY = 10
        buyStockPostData = self.get_buy_stock_post_data_dict(self.produto.id, self.supplier.id, STOCK_TO_BUY)

        response = self.client.post(reverse("products:buyStock"), data = buyStockPostData, follow=True)
        self.assertEqual(response.context['myproducts'][0]['stock'], STOCK_TO_BUY)
    
    def test_cant_buy_stock_for_product_without_supplier(self):
        
        STOCK_TO_BUY = 10
        buyStockPostData = self.get_buy_stock_post_data_dict(self.produto.id, self.supplier.id, STOCK_TO_BUY)

        response = self.client.post(reverse("products:buyStock"), data = buyStockPostData, follow=True)
        self.assertEqual(response.context['product'].stock, 0)
    
    def test_can_buy_product_as_client(self):
        
        associatePostData = self.get_associate_post_data_dict(self.supplier.id, self.produto.id) 
        self.client.post(reverse("suppliers:register_products_to_supplier"), data = associatePostData, follow=True)

        STOCK_TO_BUY = 10
        buyStockPostData = self.get_buy_stock_post_data_dict(self.produto.id, self.supplier.id, STOCK_TO_BUY)

        self.client.post(reverse("products:buyStock"), data = buyStockPostData, follow=True)
        QT_TO_BUY = 2
        buyProductClientPostData = self.get_buy_product_as_client_post_data_dict(QT_TO_BUY)
        
        response = self.client.post(reverse("products:buyProduct", kwargs={'id':self.produto.id}), data = buyProductClientPostData,
                                    follow=True)

        self.assertTrue(response.context['myproduct'].stock == STOCK_TO_BUY-QT_TO_BUY)
        self.assertTrue(response.context['myproduct'].sold == QT_TO_BUY)

    def test_cant_buy_more_than_stock_of_product_as_client(self):
        associatePostData = self.get_associate_post_data_dict(self.supplier.id, self.produto.id) 

        self.client.post(reverse("suppliers:register_products_to_supplier"), data = associatePostData, follow=True)

        STOCK_TO_BUY = 10
        buyStockPostData = self.get_buy_stock_post_data_dict(self.produto.id, self.supplier.id, STOCK_TO_BUY)

        self.client.post(reverse("products:buyStock"), data = buyStockPostData, follow=True)

        QT_TO_BUY = 100
        buyProductClientPostData = self.get_buy_product_as_client_post_data_dict(QT_TO_BUY)
        
        response = self.client.post(reverse("products:buyProduct", kwargs={'id':self.produto.id}), data = buyProductClientPostData,
                                    follow=True)

        self.assertTrue(response.context['myproduct'].stock == STOCK_TO_BUY)
        self.assertTrue(response.context['myproduct'].sold == 0)