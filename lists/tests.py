from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
# from django.template.loader import render_to_string

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_home_page_return_correct_html(self):

        #vo和v1，v2的功能一致
        #--------------v0 start -------------
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.endswith('</html>'))
        # --------------v0 end -------------

        # --------------v1 start -------------
        # request = HttpRequest()
        # response = home_page(request)
        # html = response.content.decode('utf8')
        # expected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)
        # --------------v1 end -------------

        # --------------v2 start -------------
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_can_save_a_POST_request(self):

        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertIn('A new list item', response.content.decode())

        self.assertTemplateUsed(response, 'home.html')