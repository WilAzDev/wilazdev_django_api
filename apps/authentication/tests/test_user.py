from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps
from django.core import mail
from datetime import datetime, timedelta

class UserRegisterTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_register')
        self.User = apps.get_model('authentication','User')
        self.data = {
            'username': 'testuser2024',
            'email': 'testuser@example.com',
            'password': 'Password@1234567',
            'password2': 'Password@1234567'
        }
        
    def delete_user(self):
        self.User.objects.all().delete()
        
    def test_register_with_valid_data(self):
        
        data = {**self.data}
        
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED,'The user was not created')
        self.assertEqual(self.User.objects.count(),1,'The user was not created')
    
        user = self.User.objects.get(username=data['username'])
        self.assertFalse(user.is_active,'The field is_active is set to True')
        self.assertFalse(user.is_staff, 'The field is_staff is set to True')
        self.assertFalse(user.is_superuser, 'The field is_superuser is set to True')
    
    def test_register_with_invalid_username(self):
        
        data = {**self.data}
        
        del data['username']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must be required')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'a'*151
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must be at most 150 characters long')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = '1testuser'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The username must not start with a number')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'te'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The username must be at least 3 characters long')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'test@123456789'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must not contain any special characters')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'test 123456789'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must not contain any spaces')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'testuser2024'
        self.client.post(self.url,data,format='json')
        data['email']='testuser2@example.com'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must be unique')
        self.assertIn('username',response.data,'Should return the error message')

    def test_register_with_invalid_email(self):
        
        data = {**self.data}
        self.client.post(self.url,data,format='json')
        data['username'] = 'testuser2025'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be unique')
        self.assertIn('email',response.data,'Should return the error message')
        self.delete_user()
        
        del data['email']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be required.')
        self.assertIn('email',response.data,'Should return the error message')
        
        data['email'] = 'testuserexample.com'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be a valid email address')
        self.assertIn('email',response.data,'Should return the error message')
        
        data['email'] = f'testuser1{"25"*117}@example.com'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be at most 254 characters long')
        self.assertIn('email',response.data,'Should return the error message')
        
    def test_register_with_invalid_password(self):
        
        data = {**self.data}
        
        data['password'] = 'password@123456789'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The password must contain at least one capital letter.')
        self.assertIn('password',response.data,'Should return the error message')
        
        data['password'] = 'Password123456789'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The password must contain at least one special character')
        self.assertIn('password',response.data,'Should return the error message')
        
        data['password'] = 'Password@abcdefghijk'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The password must contain at least one digit')
        self.assertIn('password',response.data,'Should return the error message')
        
        
        data['password'] = f'Password@{'0'*6}'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The password must be at least characters long')
        self.assertIn('password',response.data,'Should return the error message')
        
        data['password'] = f'Password@{'0'*120}'
        data['password2'] = data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The password must be at most 128 characters long')
        self.assertIn('password',response.data,'Should return the error message')
        
        data['password'] = 'Password@123456789'
        data['password2'] = f'{data["password"]}000'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The passwords must match')
        self.assertIn('password2',response.data,'Should return the error message')
        
        del data['password2']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The password2 field is required')
        self.assertIn('password2',response.data,'Should return the error message')
        
        data['password2'] = 'Password@123456789'
        del data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The password field is required')
        self.assertIn('password',response.data,'Should return the error message')
        
    def test_token_present_in_email_template(self):
        
        self.client.post(self.url, self.data,format='json')
        
        self.assertEqual(len(mail.outbox),1,'Should send one email')
        email = mail.outbox[0]
        activation_link = email.alternatives[0][0].split('href="')[1].split('"')[0]
        
        token = activation_link.split('/activate/')[1].strip('/')
                
        try:
            decoded_token = AccessToken(token)
        except Exception as e:
            self.fail(f'Invalid token: {e}')
            
        iat_time = datetime.fromtimestamp(decoded_token['iat'])
        exp_time = datetime.fromtimestamp(decoded_token['exp'])
        
        token_duration = exp_time - iat_time
        expected_duraction = timedelta(minutes=30)
        
        self.assertAlmostEqual(
            token_duration.total_seconds(),
            expected_duraction.total_seconds(),
            delta=1,
            msg='The token duration is not 30 minutes'
        )

class UserActivateTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_activate')
        self.User = apps.get_model('authentication','User')
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@123456789',
            is_active=False
        )
        self.token = AccessToken.for_user(self.user)
        self.token.set_exp(
            from_time=datetime.now(),
            lifetime=timedelta(minutes=30)
        )
    
    def test_activation_with_valid_token(self):
        
        response = self.client.post(self.url,{'activation_token':str(self.token)})
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The request should return 200 OK')
        self.user = self.User.objects.filter(id=self.user.id).first()
        self.assertTrue(self.user.is_active,'The user is not activated')
            
    def test_activation_with_invalid_token(self):
        
        response = self.client.post(self.url,{'activation_token':'invalid_token'})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The token must be a valid token')
        self.assertFalse(self.user.is_active,'The user is activated')
        
        token = AccessToken.for_user(self.user)
        payload = token.payload
        payload['exp'] = datetime.now()- timedelta(seconds=5)
        payload['iat'] = datetime.now()- timedelta(seconds=1)
        expired_token = AccessToken.for_user(self.user)
        expired_token.payload = payload
        response = self.client.post(self.url,{'activation_token':expired_token})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The token must not be expired')
        self.assertFalse(self.user.is_active,'The user is activated')
        
    def test_activation_with_no_token(self):
        
        response = self.client.post(self.url,{})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The response status code is not 400')
        self.assertFalse(self.user.is_active,'The user is activated')
        