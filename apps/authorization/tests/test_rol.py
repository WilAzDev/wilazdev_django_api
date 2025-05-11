from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps

class RolCreateTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('roles-create')
        self.User = apps.get_model('authentication','User')
        self.Role = apps.get_model('authorization','Role')
        self.data = {
            'name': 'TEST ROLE',
        }
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@1234567',
            is_active=True
        )
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        
    def test_rol_create_with_valid_data(self):
        data = {**self.data}
        
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED,'The role was not created')
        self.assertEqual(self.Role.objects.count(),1,'The role was not registered on the database')        
        expected_name = self.data['name'].lower().replace(' ', '_')
        self.assertEqual(response.data.get('name'),expected_name,'The role name was not returned correctly')
    
    def test_rol_create_with_invalid_name(self):
        data = {**self.data}
        
        self.client.post(self.url,self.data,format='json')
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with an existing name')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),2,'Two roles were created with the same name')
        
        data['name'] = ''
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with an empty name')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),2,'The role was registered with and empty name on the database')
        
        data['name'] = 'test@ rol'
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with a name that contains special characters')
        self.assertIn('name',response.data,'Should return an error message for the name field')

        self.assertNotEqual(self.Role.objects.count(),2,'The role was registered with a name that contains special characters on the database')
        
        data['name'] = 'test1 rol'
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with a name that contains numbers')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),2,'The role was registered with a name that contains numbers on the database')
        
        data['name'] = f'test{"a"*21}'
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with a name that contains more than 30 characters')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),2,'The role was registered with a name that contains more than 30 characters on the database')
        