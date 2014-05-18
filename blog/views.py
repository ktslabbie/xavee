from .models import Post
from django.views.generic import ListView, DetailView

class PublishedPostsMixin(object):
    def get_queryset(self):
        return self.model.objects.live()

class PostListMixin(PublishedPostsMixin, ListView):
    model = Post

class PostDetailMixin(PublishedPostsMixin, DetailView):
    model = Post
