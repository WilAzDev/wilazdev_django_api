from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from django.apps import apps
from django.core import mail
from datetime import datetime, timedelta
from ..functions import (
    token
)
from ..choices import (
    PasswordRecoveryChoises
)

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

class UserUpdateTests(APITestCase):
    
    def setUp(self):
        self.User = apps.get_model('authentication','User')
        self.create_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Password@123456789',
            'is_active': True,
        }
        self.user = self.User.objects.create_user(**self.create_data)
        self.url = reverse('auth_user_update', kwargs={'pk': self.user.id})
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        self.update_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
        }
    
    def test_user_update_with_valid_data(self):
        
        data = {**self.update_data}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The user must be updated')
        user = self.User.objects.get(id=self.user.id)
        self.assertEqual(user.username, self.update_data['username'],'The username was not updated')
        self.assertEqual(user.email, self.update_data['email'],'The email was not updated')
    
    def test_user_update_with_invalid_username(self):
        
        data = {**self.update_data}
        
        del data['username']
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must be required')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'a'*151
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must be at most 150 characters long')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = '1testuser'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The username must not start with a number')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'te'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The username must be at least 3 characters long')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'test@123456789'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must not contain any special characters')
        self.assertIn('username',response.data,'Should return the error message')
        
        data['username'] = 'test 123456789'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must not contain any spaces')
        self.assertIn('username',response.data,'Should return the error message')
        
        data_user_two = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'Password@12345678',
            'is_active': True,
        }
        self.User.objects.create_user(**data_user_two)
        data['username'] = 'testuser2'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The username must be unique')
        self.assertIn('username',response.data,'Should return the error message')

    def test_user_update_with_invalid_email(self):
        
        data = {**self.update_data}
        data_user_two = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'Password@12345678',
            'is_active': True,
        }
        self.User.objects.create_user(**data_user_two)
        data['email'] = 'testuser2@example.com'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be unique')
        self.assertIn('email',response.data,'Should return the error message')
        
        del data['email']
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be required.')
        self.assertIn('email',response.data,'Should return the error message')
        
        data['email'] = 'testuserexample.com'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be a valid email address')
        self.assertIn('email',response.data,'Should return the error message')
        
        data['email'] = f'testuser1{"25"*117}@example.com'
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST, 'The email must be at most 254 characters long')
        self.assertIn('email',response.data,'Should return the error message')

    def test_user_update_witch_invalid_user(self):
        
        data = {**self.update_data}
        self.access_token = ''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.put(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,'The user must be authenticated')
        
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
        self.assertIn('activation_token',response.data,'Should return the token error')

        token = AccessToken.for_user(self.user)
        payload = token.payload
        payload['exp'] = datetime.now()- timedelta(seconds=5)
        payload['iat'] = datetime.now()- timedelta(seconds=1)
        expired_token = AccessToken.for_user(self.user)
        expired_token.payload = payload
        response = self.client.post(self.url,{'activation_token':expired_token})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The token must not be expired')
        self.assertFalse(self.user.is_active,'The user is activated')
        self.assertIn('activation_token',response.data,'Should return the token error')
        
    def test_activation_with_no_token(self):
        
        response = self.client.post(self.url,{})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The response status code is not 400')
        self.assertFalse(self.user.is_active,'The user is activated')
        self.assertIn('activation_token',response.data,'Should return the token error')

class UserLoginTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_login')
        self.User = apps.get_model('authentication','User')
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@123456789',
            is_active=True
        )
        self.data = {'username':self.user.username,'password':'Password@123456789'}
    
    def test_login_with_valid_credentials(self):
        
        data = {**self.data}
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The user could not login successfully')
        self.assertIsNotNone(response.data.get('access_token'),'Should return the access token')
        decoded_token = AccessToken(response.data.get('access_token'))
        iat_time = datetime.fromtimestamp(decoded_token['iat'])
        exp_time = datetime.fromtimestamp(decoded_token['exp'])
        token_duration = exp_time - iat_time
        expected_duration = timedelta(minutes=15)
        self.assertAlmostEqual(
            token_duration.total_seconds(),
            expected_duration.total_seconds(),
            delta=1,
            msg='The access_token duration is not 15 minutes'
        )
        self.assertIsNotNone(response.data.get('refresh_token'),'Should return the refresh token')
        decoded_token = RefreshToken(response.data.get('refresh_token'))
        iat_time = datetime.fromtimestamp(decoded_token['iat'])
        exp_time = datetime.fromtimestamp(decoded_token['exp'])
        token_duration = exp_time - iat_time
        expected_duration = timedelta(days=1)
        self.assertAlmostEqual(
            token_duration.total_seconds(),
            expected_duration.total_seconds(),
            delta=1,
            msg='The refresh_token duration is not 1 day'
        )
        self.assertIn('token_type',response.data,'Should return the token type')
        self.assertIn('expires_in',response.data,'Should return the token expiration time')
        self.assertIn('refresh_expires_in',response.data,'Should return the refresh token expiration time')
        
        del data['username']
        data['email'] = self.user.email
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The user could not login successfully')
        
    def test_login_with_invalid_credentials(self):
        
        data = {**self.data}
        
        del data['password']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The user must not login successfully')
        self.assertIn('password',response.data,'Should return the password error')
        
        data["password"] = "INVALID_PASSWORD"
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,'The user should not be able to login with invalid credentials')
        data['password'] = self.data['password']
        
        data['username'] = "INVALID_USERNAME"
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,'The user should not be able to login with invalid credentials')
        del data['username']
                
        data['email'] = 'invalidemail@gmail.com'
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,'The user should not be able to login with invalid credentials')
        
        del data['email']
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The user should not be able to login with invalid credentials')
        self.assertIn('email_or_username',response.data,'If the request does not have the email it must have the username')
    
    def test_login_for_inactive_user(self):
        
        user = self.User.objects.create_user(
            username=f"{self.data['username']}2",
            email='test2@gmail.com',
            password=self.data['password'],
            is_active=False
        )
        
        data = {'username':user.username,'password':user.password}
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,'The user should not be able to login with an inactive account')

class UserLogoutTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_logout')
        self.User = apps.get_model('authentication','User')
        self.user_data = {
            'username':'testuser',
            'email':'test@gmail.com',
            'password':'Password@980320'
        }
        self.user = self.User.objects.create_user(**self.user_data)
        self.auth_data = {'username':self.user_data['username'],'password':self.user_data['password']}
        self.auth_response = self.client.post(reverse('auth_login'),self.auth_data)
        self.access_token = self.auth_response.data['access_token']
        self.refresh_token = self.auth_response.data['refresh_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.access_token)
        
    def test_logout(self):
        response = self.client.post(self.url,{'refresh':self.refresh_token})
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT,'The user should be able to logout')
        self.assertFalse(token.is_token_valid(self.refresh_token),'The refresh_token must be invalid after logout')
        
class UserRefreshTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_refresh')
        self.auth_url = reverse('auth_login')
        self.User = apps.get_model('authentication','User')
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@123456789',
            is_active=True
        )
        self.login_data = {'username':self.user.username,'password':'Password@123456789'}
    
    def test_refresh_valid_token(self):
        
        login_response = self.client.post(self.auth_url,self.login_data,format='json')
        data = {'refresh':login_response.data.get('refresh_token')}
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK,'The user should be able to refresh their token')
        self.assertIsNotNone(response.data.get('access_token'),'Should return the access token')
        decoded_token = AccessToken(response.data.get('access_token'))
        iat_time = datetime.fromtimestamp(decoded_token['iat'])
        exp_time = datetime.fromtimestamp(decoded_token['exp'])
        token_duration = exp_time - iat_time
        expected_duration = timedelta(minutes=15)
        self.assertAlmostEqual(
            token_duration.total_seconds(),
            expected_duration.total_seconds(),
            delta=1,
            msg='The access_token duration is not 15 minutes'
        )
        self.assertIsNotNone(response.data.get('refresh_token'),'Should return the refresh token')
        decoded_token = RefreshToken(response.data.get('refresh_token'))
        iat_time = datetime.fromtimestamp(decoded_token['iat'])
        exp_time = datetime.fromtimestamp(decoded_token['exp'])
        token_duration = exp_time - iat_time
        expected_duration = timedelta(days=1)
        self.assertAlmostEqual(
            token_duration.total_seconds(),
            expected_duration.total_seconds(),
            delta=1,
            msg='The refresh_token duration is not 1 day'
        )
        self.assertIn('token_type',response.data,'Should return the token type')
        self.assertIn('expires_in',response.data,'Should return the token expiration time')
        self.assertIn('refresh_expires_in',response.data,'Should return the refresh token expiration time')
    
    def test_refresh_token_with_no_token(self):
        
        data = {}
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The user should not be able to refresh their token without a token')
        self.assertIn('refresh',response.data,'Should return the refresh token error')
    
    def test_refresh_token_expired(self):
        auth_response = self.client.post(self.auth_url, self.login_data, format='json')
        refresh_token = RefreshToken(auth_response.data['refresh_token'])
        
        refresh_token.set_exp(lifetime=timedelta(seconds=-5))
        
        data = {'refresh': str(refresh_token)}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserRequestChangePasswordTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_request_password_change')
        self.User = apps.get_model('authentication', 'User')
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@123456789',
            is_active=True
        )
        self.password_change_data = {'email': self.user.email,'motive':PasswordRecoveryChoises.RECOVERY}
    
    def test_request_password_change(self):
        
        self.client.post(self.url, self.password_change_data, format='json')
        self.assertEqual(len(mail.outbox),1,'Should send a password change email')
        email = mail.outbox[0]
        password_link = email.alternatives[0][0].split('href="')[1].split('"')[0]
        token = password_link.split('/reset-password/')[1].strip('/')
        try:
            decoded_token = AccessToken(token)
        except Exception as e:
            self.fail(f"Token decoding failed: {str(e)}")
        
        iat_time = datetime.fromtimestamp(decoded_token['iat'])
        exp_time = datetime.fromtimestamp(decoded_token['exp'])
        
        token_duration = exp_time - iat_time
        expected_duration = timedelta(minutes=5)
        
        self.assertAlmostEqual(
            token_duration.total_seconds(),
            expected_duration.total_seconds(),
            delta=1,
            msg='The password change token duration is not 5 minutes'
        )
    
    def test_request_password_change_with_invalid_email(self):
        
        data = {**self.password_change_data}
        data['email'] = 'invalidemail@example.com'
        request = self.client.post(self.url, data, format='json')
        self.assertEqual(request.status_code,status.HTTP_200_OK,'Should not said if the email not exist')
        self.assertEqual(len(mail.outbox), 0, 'Should not send an email for an invalid email address')
    
    def test_request_password_change_with_invalid_motive(self):
        data = {**self.password_change_data}
        data['motive'] = 'InvalidMotive'
        request = self.client.post(self.url,data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST, 'Should return an error for an invalid motive')
        self.assertIn('motive', request.data, 'Should return an error message for an invalid motive')

class UserChangePasswordTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('auth_change_password')
        self.User = apps.get_model('authentication', 'User')
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@123456789', 
            is_active=True
        )
        self.token = AccessToken.for_user(self.user)
        self.token.set_exp(
            from_time=datetime.now(),
            lifetime=timedelta(minutes=5)
        )
        self.password_data = {
            'password': 'NewPassword@123456',
            'password2': 'NewPassword@123456',
            'recovery_token': str(self.token)
        }
    
    def test_change_password(self):
        
        response = self.client.post(self.url, self.password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'The user should be able to change their password successfully')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password_data['password']), 'The new password should be set correctly')
        
    def test_change_password_with_invalid_password(self):
        
        data = {**self.password_data}
        
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