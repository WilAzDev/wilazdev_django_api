from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User

# Create your tests here.
class UserRegisterTests(APITestCase):
    def setUp(self):
        self.url = reverse('auth_register')
        
    def test_register_with_valid_data(self):
        
        data = {
            'username': 'testuser2024',
            'email': 'testuser@example.com',
            'password': 'Password@1234567',
            'password2': 'Password@1234567'
        }
        
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        user = User.objects.get(username=data['username'])
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_register_with_invalid_username(self):
        
        data = {
            'username': '1testuser',
            'email': 'testuser@example.com',
            'password': 'Password@123456789',
            'password2': 'Password@123456789'
        }
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('username',response.data)
        
        data['username'] = 'te'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('username',response.data)
        
        data['username'] = 'te12345678901234567890'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('username',response.data)
        
        data['username'] = 'test@123456789'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('username',response.data)
        
        data['username'] = 'test 123456789'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('username',response.data)
        
        data['username'] = 'testuser2024'
        self.client.post(self.url,data,format='json')
        data['email']='testuser2@example.com'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('username',response.data)

    def test_register_with_invalid_email(self):
        
        data = {
            'username': 'testuser',
            'email': 'testuserexample.com',
            'password': 'Password@123456789',
            'password2': 'Password@123456789'
        }
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('email',response.data)
        
        data['email'] = f'testuser1{'25'*117}@example.com'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('email',response.data)
        
    def test_register_with_invalid_password(self):
        
        data = {
            'username': 'testuser2024',
            'email': 'testuser@example.com',
            'password': 'password@123456789',
            'password2': 'password@123456789'
        }
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('password',response.data)
        
        data['password'] = 'Password123456789'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('password',response.data)
        
        data['password'] = 'Password@abcdefghijk'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('password',response.data)
        
        data['password'] = 'Password12345678900'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('password',response.data)
        
        data['password'] = f'Password@{'0'*6}'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('password',response.data)
        
        data['password'] = f'Password@{'0'*120}'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('password',response.data)
        
        data['password'] = 'Password@123456789'
        data['password2'] = f'{data["password"]}000'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('password',response.data)