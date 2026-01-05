from django.test import TestCase
from django.urls import reverse
from .models import Product, Company


# Create your tests here.


class ProductsTestCase(TestCase):
    def test_no_products_found(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertContains(response, 'no products found!')

    def test_product_list_detail(self):
        company = Company.objects.create(name='company')
        product1 = Product.objects.create(name='product1', price='100 $', description='describe1', company=company)
        Product.objects.create(name='product2', price='200 $', description='describe2', company=company)
        Product.objects.create(name='product3', price='300 $', description='describe3', company=company)
        #poduct list
        response = self.client.get(reverse('products:product_list'))
        products = Product.objects.all()
        for product in products:
            self.assertContains(response, product.name)
        #product detail
        response = self.client.get(reverse('products:product_detail', kwargs={'id':product1.id}))
        self.assertContains(response, product1.name)
        self.assertContains(response, product1.price)
        self.assertContains(response, product1.description)