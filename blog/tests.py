# from django.core.urlresolvers import resolve, reverse
# from django.http import HttpRequest
# from django.test import TestCase
# from blog.views import PostListView, PostDetailView
# from blog.models import Post
# import importlib

# Create your tests here.
# class SmokeTest(TestCase):
    
#     def test_url_resolution(self):
#         ''' Test to make sure the right URLs call the right class-based views. '''
#         self.assertEqual(self.get_cbv_from_url_name('blog:post-list'), PostListView)
#         
#     def test_post_list_returns_correct_html(self):
#         ''' Test whether the correct HTML is being returned. '''
#         response = self.client.get(reverse('blog:post-list'))
#         self.assertEquals(response.status_code, 200)
#         self.assertIn(b'<ul class="post-list">', response.content)
#         
#         
#     def get_cbv_from_url_name(self, name):
#         ''' Helper function to obtain the Class-Based View class from a URL name. '''
#         view_func = resolve(reverse(name)).func
#         module = importlib.import_module(view_func.__module__)
#         return getattr(module, view_func.__name__)