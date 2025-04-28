from django.test import TestCase
from django.urls import reverse
from goods.models import Goods
from http import HTTPStatus


# Create your tests here.
class GetPagesTestCse(TestCase):
    fixtures = ['goods_goods.json']
    def setUp(self):
        "Инициализация перед выполнением каждого теста"
        return super().setUp()
    
    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'goods/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add-prod')
        redirect_uri = reverse("users:login") + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        g_lst = Goods.manager.all()
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['goods'], g_lst)

    def tearDown(self):
        "Действия после выполнения каждого теста"
        return super().tearDown()