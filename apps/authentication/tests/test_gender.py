from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps

class GenderTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('gender_list')
    
    def test_gender_endpoint(self):
        User = apps.get_model('authentication','User')
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@12345678'
        )
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_gender_endpoint_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)