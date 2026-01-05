from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
# Create your tests here.


class RegistrationTestCase(TestCase):
    def test_account_created(self):
        self.client.post(
            reverse('accounts:register'),
            data = {
                'username':'Ismoil',
                'first_name':'Ismoiljon',
                'last_name':'Abdumajidov',
                'email':'ismoil2@gmail.com',
                'password':'ismoiljon2003'
            }
        )
        response = self.client.post(
            reverse('accounts:register'),
            data={
                'username': 'Ismoil',
                'password': 'ismoiljon2003'
            }
        )
        user = CustomUser.objects.get(username='Ismoil')
        count = CustomUser.objects.count()
        self.assertEqual(user.username, 'Ismoil')
        self.assertEqual(user.first_name, 'Ismoiljon')
        self.assertEqual(user.last_name, 'Abdumajidov')
        self.assertEqual(user.email, 'ismoil2@gmail.com')
        self.assertNotEqual(user.password, 'ismoiljon2003')
        self.assertTrue(user.check_password('ismoiljon2003'))
        self.assertEqual(count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    def test_required_fields(self):
        response = self.client.post(
            reverse('accounts:register'),
            data={
                'email':'invalid-email',
                'first_name':'super'
            }
        )
        count = CustomUser.objects.count()
        self.assertEqual(count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')


class TestLoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='ismoil')
        self.db_user.set_password('ismoiljon2003')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('accounts:login'),
            data={
                'username':'ismoil',
                'password':'ismoiljon2003'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        response = self.client.post(
            reverse('accounts:login'),
            data={
                'username':'wrong-username',
                'password':'ismoiljon2003'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.', status_code=200)

        response = self.client.post(
            reverse('accounts:login'),
            data={
                'username':'ismoil',
                'password':'wrong-password'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.', status_code=200)

    def test_logout(self):
        self.client.login(username='ismoil', password='ismoiljon2003')
        self.client.get(reverse('accounts:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class TestProfileTestCase(TestCase):
    def test_not_authenticated(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:login') + '?next=/accounts/profile/')

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username='ismoil',
            first_name='first_name',
            last_name='last_name',
            email='email@gmail.com'
        )
        user.set_password('Ismoiljon2003')
        user.save()
        self.client.login(username='ismoil', password='Ismoiljon2003')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_profile_update(self):
        user = CustomUser.objects.create(username='Ismoil', first_name='Ismoiljon', last_name='john', email='john21@gmail.com')
        user.set_password('Ismoiljon2003')
        user.save()
        self.client.login(username='Ismoil', password='Ismoiljon2003')
        response = self.client.post(
            reverse('accounts:profile-update'),
            data={
                'username':'Ismoil',
                'first_name':'Ismoiljon1',
                'last_name':'john',
                'email':'john212@gmail.com'
            }
        )
        user.refresh_from_db()
        # self.assertEqual(response.url, reverse('accounts:profile'))
        self.assertEqual(user.first_name, 'Ismoiljon1')
        self.assertEqual(user.email, 'john212@gmail.com')
