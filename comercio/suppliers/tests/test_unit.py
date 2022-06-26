from django.test import TestCase
from ..models import Supplier
from django.urls import reverse

class Utils():
    @staticmethod
    def getDictOfSupplier(name, tel, cnpj, address):
        return  {
            'name': name,
            'telephone': tel,
            'cnpj': cnpj,
            'address': address
        }

class SupplierIndexViewTests(TestCase):
    def test_index_no_suppliers_warning(self):
        """
        Testa se aparece uma mensagem de erro apropriada quando não houverem Suppliers cadastrados
        """
        response = self.client.get(reverse("suppliers:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não existem fornecedores cadastrados.")
        self.assertQuerysetEqual(response.context['suppliers_list'], [])

    def test_new_supplier_sent_to_index(self):
        """
        Testa se o supplier recém cadastrado é enviado para a página de index
        """
        supName = "Fornecedor"
        supTel = "(31) 12345-6789"
        supCnpj = '1234567890'
        supAddress = "Rua Teste"

        novoSupplier = Supplier.objects.create(name=supName, telephone=supTel, cnpj=supCnpj, address=supAddress)

        response = self.client.get(reverse("suppliers:index"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['suppliers_list'][0], novoSupplier)

class SaveSupplierViewTests(TestCase):

    def test_registered_supplier_sent_to_index(self):
        """
        Testa se o fornecedor cadastrado na tela de cadastro é enviado para o index
        """
        supName = "Fornecedor"
        supTel = "(31) 12345-6789"
        supCnpj = '1234567890'
        supAddress = "Rua Teste"

        postData = Utils.getDictOfSupplier(supName, supTel, supCnpj, supAddress)

        novoSup = Supplier(name = supName, telephone = supTel, cnpj = supCnpj, address = supAddress)

        response = self.client.post(reverse("suppliers:supplierregistry"), data = postData, follow=True)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('suppliers:index'))
        postData['id'] = 1
        self.assertEqual(response.context['suppliers_list'][0], novoSup)
    
    def test_cant_register_supplier_invalid_info(self):
        """
        Testa se o supplier não é criado se o formulário não for preenchido corretamente
        """
        supName = ""
        supTel = "(31) 12345-6789"
        supCnpj = ''
        supAddress = "Rua Teste"

        postData = Utils.getDictOfSupplier(supName, supTel, supCnpj, supAddress)

        response = self.client.post(reverse("suppliers:supplierregistry"), data = postData, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Supplier.objects.count(), 0)
        self.assertContains(response, 'This field is required')

class DeleteSupplierViewTest(TestCase):
    def test_can_delete_supplier(self):
        supName = "Fornecedor"
        supTel = "(31) 12345-6789"
        supCnpj = '1234567890'
        supAddress = "Rua Teste"

        novoSupplier = Supplier.objects.create(name=supName, telephone=supTel, cnpj=supCnpj, address=supAddress)

        response = self.client.post(reverse("suppliers:delete", kwargs={'pk':novoSupplier.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Supplier.objects.count(), 0)
    
    def test_cant_delete_supplier_that_doesnt_exists(self):
        response = self.client.post(reverse("suppliers:delete", kwargs={'pk':1}), follow=True)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Supplier.objects.count(), 0)

class AtualizarFornecedorViewTest(TestCase):
    
    def test_update_supplier(self):
        supName = "Fornecedor"
        supTel = "(31) 12345-6789"
        supCnpj = '1234567890'
        supAddress = "Rua Teste"

        novoSupplier = Supplier.objects.create(name=supName, telephone=supTel, cnpj=supCnpj, address=supAddress)

        supDict = Utils.getDictOfSupplier(supName, supTel, supCnpj, supAddress)
        supDict['address'] = 'Bairro teste'

        response = self.client.post(reverse("suppliers:update", kwargs={'pk':novoSupplier.id}), data=supDict, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Supplier.objects.get(pk=novoSupplier.id).address, supDict['address'])
    
    def test_cant_update_supplier_that_doesnt_exists(self):
        response = self.client.post(reverse("suppliers:update", kwargs={'pk':1}), follow=True)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Supplier.objects.count(), 0)
    
    def test_cant_update_supplier_invalid_info(self):
        """
        Testa se o supplier não é atualizado se o formulário não for preenchido corretamente
        """
        supName = "Teste"
        supTel = "(31) 12345-6789"
        supCnpj = '123'
        supAddress = "Rua Teste"

        novoProduto = Supplier.objects.create(name = supName, telephone = supTel, cnpj=supCnpj, address=supAddress)
        postData = Utils.getDictOfSupplier(supName, supTel, supCnpj, supAddress)

        postData['name'] = ""
        response = self.client.post(reverse("suppliers:update", kwargs={'pk':novoProduto.id}), data = postData, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(Supplier.objects.get(pk=novoProduto.id).name, supName)
        

class SupplierSearchViewTests(TestCase):
    def test_cant_find_suppliers_that_doesnt_exists(self):
        """
        Testa se aparece uma mensagem de erro apropriada quando não houver resultado para a pesquisa
        """
        response = self.client.get(reverse("suppliers:search"), data={'name':'a'})
        self.assertEqual(response.status_code, 200)
        noResultsMsg = 'Não existem fornecedores cadastrados com o nome pesquisado.'
        self.assertContains(response, noResultsMsg)
        self.assertQuerysetEqual(response.context['suppliers_list'], [])

    def test_can_find_registered_supplier(self):
        """
        Testa se o supplier recém cadastrado é enviado para a página de index
        """
        supName = "Fornecedor Teste"
        supTel = "(31) 12345-6789"
        supCnpj = '1234567890'
        supAddress = "Rua Teste"

        novoSupplier = Supplier.objects.create(name=supName, telephone=supTel, cnpj=supCnpj, address=supAddress)

        response = self.client.get(reverse("suppliers:search"), data={'name':novoSupplier.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, novoSupplier.name)
        self.assertContains(response, novoSupplier.telephone)
        self.assertContains(response, novoSupplier.cnpj)
        self.assertContains(response, novoSupplier.address)