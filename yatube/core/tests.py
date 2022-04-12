from http import HTTPStatus

from django.test import Client, TestCase


class ErrorTestClass(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()

    def test_url_returns_404_error(self):
        """Запрос к несуществующей странице вернёт ошибку 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertTemplateUsed(response, 'core/404.html')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
