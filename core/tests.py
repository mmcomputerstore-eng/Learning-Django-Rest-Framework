from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product


class ProductAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            is_staff=True
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_list_products(self):
        url = "/api/products/viewset/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_product(self):
        url = "/api/products/viewset/"

        data = {
            "name": "Test Mouse",
            "description": "Wireless Test Mouse",
            "price": 2500,
            "stock": 10
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.name, "Test Mouse")
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.owner, self.user)  

    def test_create_product_invalid_data(self):
        url = '/api/products/viewset/'

        data = {
        'name': '',
        'description': 'Invalid Product',
        'price': '-500',
        'stock': -10,
        }

        response = self.client.post(
        url,
        data,
        format='json'
        )

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
        )

    def test_unauthenticated_user(self):
        self.client.force_authenticate(user=None)

        url = '/api/products/viewset/'

        response = self.client.get(url)

        self.assertEqual(
        response.status_code,
        status.HTTP_401_UNAUTHORIZED
        )

    def test_user_cannot_update_other_users_product(self):
    # User B
        other_user = User.objects.create_user(
        username='otheruser',
        password='otherpassword'
    )

    # User A کے نام سے Product create کریں
        product = Product.objects.create(
        owner=self.user,
        name='Owner Product',
        description='Test Product',
        price=1000,
        stock=10
        )

    # اب User B بن جائیں
        self.client.force_authenticate(
        user=other_user
        )

        url = f'/api/products/viewset/{product.id}/'

        data = {
        'name': 'Hacked Product',
        'description': 'Trying to modify another users product',
        'price': '2000.00',
        'stock': 20
        }

        response = self.client.put(
        url,
        data,
        format='json'
        )

        self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
        )

    def test_owner_can_update_own_product(self):
        product = Product.objects.create(
        owner=self.user,
        name='My Product',
        description='My Product',
        price=1000,
        stock=10
    )

        url = f'/api/products/viewset/{product.id}/'

        data = {
        'name': 'Updated Product',
        'description': 'Updated Description',
        'price': '1500.00',
        'stock': 20
    }

        response = self.client.put(
        url,
        data,
        format='json'
    )

        self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )

        product.refresh_from_db()

        self.assertEqual(
        product.name,
        'Updated Product'
    )
    def test_owner_can_patch_own_product(self):
        product = Product.objects.create(
        owner=self.user,
        name='Original Product',
        description='Original Description',
        price=1000,
        stock=10
    )

        url = f'/api/products/viewset/{product.id}/'

        data = {
        'stock': 25
    }

        response = self.client.patch(
        url,
        data,
        format='json'
    )

        self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )

        product.refresh_from_db()

        self.assertEqual(product.stock, 25)
        self.assertEqual(product.name, 'Original Product')

        
    def test_owner_can_delete_own_product(self):
        product = Product.objects.create(
        owner=self.user,
        name='Delete Product',
        description='Product to delete',
        price=1000,
        stock=10
    )

        url = f'/api/products/viewset/{product.id}/'

        response = self.client.delete(url)

        self.assertEqual(
        response.status_code,
        status.HTTP_204_NO_CONTENT
    )

        self.assertFalse(
        Product.objects.filter(id=product.id).exists()
    )