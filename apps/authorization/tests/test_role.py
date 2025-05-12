from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps

class RoleCreateTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('role-list')
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
        self.role = self.Role.objects.filter(name='admin').first()
        self.user.assign_roles([self.role.id])
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        
    def test_role_create_with_valid_data(self):
        data = {**self.data}
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED,'The role was not created')
        self.assertEqual(self.Role.objects.count(),2,'The role was not registered on the database')        
        expected_name = self.data['name'].lower().replace(' ', '_')
        self.assertEqual(response.data.get('name'),expected_name,'The role name was not returned correctly')
    
    def test_role_create_with_invalid_name(self):
        data = {**self.data}
        
        self.client.post(self.url,self.data,format='json')
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with an existing name')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),3,'Two roles were created with the same name')
        
        data['name'] = ''
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with an empty name')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),3,'The role was registered with and empty name on the database')
        
        data['name'] = 'test@ rol'
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with a name that contains special characters')
        self.assertIn('name',response.data,'Should return an error message for the name field')

        self.assertNotEqual(self.Role.objects.count(),3,'The role was registered with a name that contains special characters on the database')
        
        data['name'] = 'test1 rol'
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with a name that contains numbers')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),3,'The role was registered with a name that contains numbers on the database')
        
        data['name'] = f'test{"a"*27}'
        response = self.client.post(self.url, data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST,'The role was created with a name that contains more than 30 characters')
        self.assertIn('name',response.data,'Should return an error message for the name field')
        self.assertNotEqual(self.Role.objects.count(),3,'The role was registered with a name that contains more than 30 characters on the database')

class RoleUpdateTests(APITestCase):
    
    def setUp(self):
        self.Role = apps.get_model('authorization', 'Role')
        self.role = self.Role.objects.create(name='test_role')
        
        self.url = reverse('role-detail', kwargs={'pk': self.role.id})
        
        self.User = apps.get_model('authentication', 'User')
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@1234567',
            is_active=True
        )
        admin_role = self.Role.objects.filter(name='admin').first()
        self.user.assign_roles([admin_role.id])
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
    
    def test_role_update_with_valid_data(self):
        data = {'name': 'UPDATED_ROLE'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Update failed with valid data')  # 200 OK expected
        
        self.role.refresh_from_db()
        self.assertEqual(self.role.name, 'updated_role', 'Name not updated in database')  # Check normalization
        
    def test_role_update_with_invalid_name(self):
        self.Role.objects.create(name='existing_role')
        
        data = {'name': 'existing_role'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Allowed duplicate name in update')
        self.assertIn('name', response.data, 'Error not linked to name field')
        
        data['name'] = 'invalid@name'
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Allowed special characters')
        
        data['name'] = 'name123'
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Allowed numbers in name')
        
        data['name'] = ''
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Allowed empty name')
        
        data['name'] = 'a' * 31
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Allowed over-length name')

class RoleDeleteTests(APITestCase):
    def setUp(self):
        self.Role = apps.get_model('authorization', 'Role')
        self.User = apps.get_model('authentication', 'User')
        
        self.role_to_delete = self.Role.objects.create(name='test_role')
        
        self.user_with_role = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password@1234567',
            is_active=True
        )
        self.user_with_role.assign_roles([self.role_to_delete.id])
        
        self.admin_user = self.User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='AdminPassword@123',
            is_active=True
        )
        admin_role = self.Role.objects.filter(name='admin').first()
        self.admin_user.assign_roles([admin_role.id])
        
        self.access_token = AccessToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        
        self.url = reverse('role-detail', kwargs={'pk': self.role_to_delete.id})

    def test_role_delete_removes_user_assignments(self):
        initial_assignment = self.user_with_role.roles.filter(id=self.role_to_delete.id).exists()
        self.assertTrue(initial_assignment, 'Role was not assigned to the user initially')
        
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Role was not deleted successfully')
        
        role_exists = self.Role.objects.filter(id=self.role_to_delete.id).exists()
        self.assertFalse(role_exists, 'Role still exists in the database')
        
        self.user_with_role.refresh_from_db()
        remaining_assignments = self.user_with_role.roles.count()
        self.assertEqual(remaining_assignments, 0, 'Role assignments were not removed')

    def test_cannot_delete_nonexistent_role(self):
        invalid_url = reverse('role-detail', kwargs={'pk': 9999})
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'Deleting a non-existent role should return 404')