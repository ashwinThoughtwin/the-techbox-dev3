from django.test import TestCase,Client
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse
from .models import Item
from .serializers import Item_Serializer
import json
from django.contrib.auth.models import User

# Create your tests here.

class ItemGetTestCase(TestCase):
    def setUp(self):
        Item.objects.create(
            name='testdata', status=True)
        Item.objects.create(
            name='testdata2', status=True)
    
    def test_01_get_items(self):
        response = self.client.get(reverse('get-items'))
        items = Item.objects.all()
        serializer = Item_Serializer(items, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SingleItemGetTestCase(TestCase):
    def setUp(self):
        self.testdata = Item.objects.create(
            name='Headphone', status=True)
        self.testdata2 = Item.objects.create(
            name='Mouse',status=True)

    def test_02_get_valid_single_item(self):
        # import pdb; pdb.set_trace()
        response = self.client.get(
            reverse('single-items', kwargs={'pk': self.testdata.pk}))
        items = Item.objects.get(pk=self.testdata.pk)
        serializer = Item_Serializer(items)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_03_get_invalid_single_item(self):
        response = self.client.get(
            reverse('single-items',kwargs={'pk':40}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewItemTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'name': 'connectors',
            'status': False
        }
        self.invalid_data = {
            'name': '',
            'status':True
        }

    def test_04_create_valid_item(self):
        response = self.client.post(
            reverse('get-items'),
            data = self.valid_data,
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_05_create_invalid_item(self):
        response = self.client.post(
            reverse('get-items'),
            data=self.invalid_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleItemTest(TestCase):

    def setUp(self):
        self.testdata = Item.objects.create(
            name='Headphone', status=True)
        self.testdata2 = Item.objects.create(
            name='Mouse', status=False)

        self.valid_data = {
            'name': 'Headphone',
            'status': False
        }
        self.invalid_data = {
            'name': '',
            'status':'False'
        }

    def test_06_valid_update_item(self):
        response = self.client.put(
            reverse('single-items', kwargs={'pk': self.testdata.pk}),
            data = self.valid_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_07_invalid_update_item(self):
        response = self.client.put(
            reverse('single-items', kwargs={'pk': self.testdata.pk}),
            data= self.invalid_data,
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleItemTest(TestCase):

    def setUp(self):
        self.testdata = Item.objects.create(
            name='HP', status=True)
        self.testdata1 = Item.objects.create(
            name='Lenovo', status=False)

    def test_08_valid_delete_item(self):
        response = self.client.delete(
            reverse('single-items', kwargs={'pk': self.testdata1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_09_invalid_delete_item(self):
        response = self.client.delete(
            reverse('single-items', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestLoginApi(TestCase):
    def setUp(self):
        User.objects.create_user('john', password='admin')
        self.valid_data = {
            "username": "john",
            "password": "admin"
        }
        self.invalid_data = {
            "username": "john",
            "password": "hiuhihi"
        }

    def test_10_valid_user_login_api(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            data = self.valid_data,
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_11_invalid_user_login_api(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            data = self.invalid_data,
            content_type='application/json')
        self.assertEqual(response.status_code,401)