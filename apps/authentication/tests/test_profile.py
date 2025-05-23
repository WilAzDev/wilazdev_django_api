from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps

class ProfileCreateTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_profile_create')
        self.User = apps.get_model('authentication','User')
        self.Gender = apps.get_model('authentication','Gender')
        self.Profile = apps.get_model('authentication','Profile')
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@1234567',
            is_active=True
        )
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        self.gender = self.Gender.objects.create(name='Test',short='T')
        self.data = {
            'first_name':'Jhon del Rio',
            'second_name':'Dóe',
            'last_name':'San',
            'second_last_name':'Jhonson',
            'gender_id':self.gender.id,
        }
        
    def delete_profile(self):
        self.Profile.objects.all().delete()
        
    def test_profile_create_with_valid_data(self):
        data = {**self.data}
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED,'The profile was not created')
        self.assertEqual(self.Profile.objects.count(), 1,'The profile must be created successfully')
        self.delete_profile()
        
        data2 = {**data}
        del data2['second_name']
        response = self.client.post(self.url,data2,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED,'The second_name must be optional')
        self.assertEqual(self.Profile.objects.count(), 1,'The profile must be created successfully')
        self.delete_profile()
        
        data3 = {**data}
        del data3['second_last_name']
        response = self.client.post(self.url,data3,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED,'The second_last_name must be optional')
        self.assertEqual(self.Profile.objects.count(), 1,'The profile must be created successfully')
        self.delete_profile()
        
        data4 = {**data}
        del data4['gender_id']
        response = self.client.post(self.url,data4,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED,'The gender_id must be optional')
        self.assertEqual(self.Profile.objects.count(), 1,'The profile must be created successfully')
        self.delete_profile()
        
    def test_profile_create_with_invalid_first_name(self):
        
        data = {**self.data}
        del data['first_name']
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must be required')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'A'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must be at least 2 characters')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = f'Jh{"o"*148}n'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must be at most 150 characters')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'jhon'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must start with a capital letter')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'Jhon2'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must not contain any numbers')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'Jhon@'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must not contain any special characters')
        self.assertIn('first_name',response.data,'Should return an error')
    
    def test_profile_create_with_invalid_second_name(self):
        
        data = {**self.data}
        
        data['second_name'] = 'A'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must be at least 2 characters long')
        self.assertIn('second_name',response.data,'Should return error message')
        
        data['second_name'] = f'D{"o"*149}e'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must be at most 150 characters long')
        self.assertIn('second_name',response.data,'Should return error message')
        
        data['second_name'] = 'dóe'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must start with a capital letter')
        self.assertIn('second_name',response.data, 'Should return error message')
        
        data['second_name'] = 'Doe2'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must not contain any numbers')
        self.assertIn('second_name',response.data,'Should return error message')
        
        data['second_name'] = 'Doe@'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must not contain any special characters')
        self.assertIn('second_name',response.data,'Should return error message')
        
    def test_profile_create_with_invalid_last_name(self):
        
        data = {**self.data}
        del data['last_name']
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name field is required')
        self.assertIn('last_name',response.data)
        
        data['last_name'] = 'A'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The last_name must be at least 2 characters long')
        self.assertIn('last_name',response.data)
        
        data['last_name'] = f'S{"o"*149}n'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must be at most 150 characters long')
        self.assertIn('last_name',response.data)
        
        data['last_name'] = 'san'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must start with a capital letter')
        self.assertIn('last_name',response.data,'Should return error message')
        
        data['last_name'] = 'San2'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must not contain any numbers')
        self.assertIn('last_name',response.data,'Should return error message')
        
        data['last_name'] = 'San@'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must not contain any special characters')
        self.assertIn('last_name',response.data,'Should return error message')
    
    def test_profile_create_with_invalid_second_last_name(self):
        
        data = {**self.data}
        
        data['second_last_name'] = 'A'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must have at least 2 characters')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = f'Jh{"o"*145}nson'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The second_last_name must be at most 150 characters long')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = 'jhonson'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must start with a capital letter')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = 'San2'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must not contain any numbers')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = 'San@'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must not contain any special characters')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
    def test_profile_create_with_invalid_user(self):
        
        data = {**self.data}
        
        self.client.post(self.url,data,format='json')
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The user must have only one profile')
        self.assertIn('user_id',response.data,'Should return error message')
        self.delete_profile()
        
        self.access_token = ''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,'The user must be authenticated')
        
    def test_profile_create_with_invalid_gender(self):
        
        data = {**self.data}
        data['gender_id'] = self.Gender.objects.all().last().id + 1
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The gender must exist')
        self.assertIn('gender_id',response.data,'Should return error message')

class ProfileUpdateTests(APITestCase):
    
    def setUp(self):
        self.User = apps.get_model('authentication','User')
        self.Profile = apps.get_model('authentication','Profile')
        self.Gender = apps.get_model('authentication','Gender')
        self.user = self.User.objects.create_user(
            username = 'testuser',
            email='test@gmail.com',
            password='Password@1321548',
            is_active=True
        )
        self.user2 = self.User.objects.create_user(
            username='testuser2', 
            email='test2@gmail.com', 
            password='Password@1321548', 
            is_active=True
        )
        self.gender = self.Gender.objects.create(
            name='Test',
            short='T'
        )
        self.gender2 = self.Gender.objects.create(
            name='Test2',
            short='T2'
        )
        self.profile = self.Profile.objects.create(
            user=self.user,
            gender=self.gender,
            first_name='Jhon',
            last_name='Doe',
        )
        self.update_data = {
            'first_name':'Jhon del Rio',
            'second_name':'Dóe',
            'last_name':'San',
            'second_last_name':'Jhonson',
            'gender_id':self.gender2.id,
        }
        self.access_token = AccessToken.for_user(self.user)
        self.access_token2 = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        self.url = reverse('auth_profile_update',kwargs={'pk': self.profile.id})
    
    def test_profile_create_with_valid_data(self):
        data = {**self.update_data}
        
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The profile was not updated')
        profile = self.Profile.objects.get(id=self.profile.id)
        self.assertEqual(profile.first_name,self.update_data['first_name'],'The first name was not updated')
        self.assertEqual(profile.second_name,self.update_data['second_name'],'The second name was not updated')
        self.assertEqual(profile.last_name,self.update_data['last_name'],'The last name was not updated')
        self.assertEqual(profile.second_last_name,self.update_data['second_last_name'],'The second last name was not updated')
        self.assertEqual(profile.gender_id,self.update_data['gender_id'],'The gender was not updated')
        
        del data['second_name']
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The second_name must be optional')
        profile = self.Profile.objects.get(id=self.profile.id)
        self.assertIsNone(profile.second_name,'The second_name must be none')
        
        del data['second_last_name']
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The second_last_name must be optional')
        self.assertIsNone(response.data['second_last_name'],'The second_last_name must be None')
        
        del data['gender_id']
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The gender_id must be optional')
        self.assertIsNone(response.data['gender_id'],'The gender must be None')
    
    def test_profile_update_with_invalid_first_name(self):
        
        data = {**self.update_data}
        del data['first_name']
        
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must be required')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'A'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must be at least 2 characters')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = f'Jh{"o"*148}n'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must be at most 150 characters')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'jhon'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must start with a capital letter')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'Jhon2'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must not contain any numbers')
        self.assertIn('first_name',response.data,'Should return an error')
        
        data['first_name'] = 'Jhon@'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The first_name must not contain any special characters')
        self.assertIn('first_name',response.data,'Should return an error')
    
    def test_profile_update_with_invalid_second_name(self):
        
        data = {**self.update_data}
        
        data['second_name'] = 'A'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must be at least 2 characters long')
        self.assertIn('second_name',response.data,'Should return error message')
        
        data['second_name'] = f'D{"o"*149}e'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must be at most 150 characters long')
        self.assertIn('second_name',response.data,'Should return error message')
        
        data['second_name'] = 'dóe'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must start with a capital letter')
        self.assertIn('second_name',response.data, 'Should return error message')
        
        data['second_name'] = 'Doe2'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must not contain any numbers')
        self.assertIn('second_name',response.data,'Should return error message')
        
        data['second_name'] = 'Doe@'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_name must not contain any special characters')
        self.assertIn('second_name',response.data,'Should return error message')
        
    def test_profile_update_with_invalid_last_name(self):
        
        data = {**self.update_data}
        del data['last_name']
        
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name field is required')
        self.assertIn('last_name',response.data)
        
        data['last_name'] = 'A'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The last_name must be at least 2 characters long')
        self.assertIn('last_name',response.data)
        
        data['last_name'] = f'S{"o"*149}n'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must be at most 150 characters long')
        self.assertIn('last_name',response.data)
        
        data['last_name'] = 'san'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must start with a capital letter')
        self.assertIn('last_name',response.data,'Should return error message')
        
        data['last_name'] = 'San2'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must not contain any numbers')
        self.assertIn('last_name',response.data,'Should return error message')
        
        data['last_name'] = 'San@'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The last_name must not contain any special characters')
        self.assertIn('last_name',response.data,'Should return error message')
    
    def test_profile_update_with_invalid_second_last_name(self):
        
        data = {**self.update_data}
        
        data['second_last_name'] = 'A'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must have at least 2 characters')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = f'Jh{"o"*145}nson'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The second_last_name must be at most 150 characters long')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = 'jhonson'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must start with a capital letter')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = 'San2'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must not contain any numbers')
        self.assertIn('second_last_name',response.data,'Should return error message')
        
        data['second_last_name'] = 'San@'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The second_last_name must not contain any special characters')
        self.assertIn('second_last_name',response.data,'Should return error message')
    
    def test_profile_update_with_invalid_gender(self):
        
        data = {**self.update_data}
        data['gender_id'] = self.Gender.objects.all().last().id + 1
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The gender must exist')
        self.assertIn('gender_id',response.data,'Should return error message')
    
    def test_profile_create_with_invalid_user(self):
        
        data = {**self.update_data}
        
        acces_token = ''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + acces_token)
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,'The user must be authenticated') 
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token2))
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN,'The user must own the profile')   