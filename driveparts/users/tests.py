from django.test import TestCase
from django.urls import reverse
from django.shortcuts import redirect
from http import HTTPStatus
from django.contrib.auth import get_user_model


# Create your tests here.
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.registration_url = reverse('users:register')  # Замените 'registration' на имя вашего URL для регистрации
        self.login_url = reverse('users:login')  # Замените 'login' на имя вашего URL для авторизации
        self.user_model = get_user_model()
        self.data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    # def test_form_register(self):
    #     path = reverse('users:register')
    #     response = self.client.get(path)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_success(self):
        
        response = self.client.post(self.registration_url, self.data, follow=True)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(self.user_model.objects.filter(username='testuser').exists())

    def test_registration_test(self):
        self.data['password2']= 'testpassword12'
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Введенные пароли не совпадают")

    

    def tearDown(self):
        "Действия после выполнения каждого теста"
        return super().tearDown()