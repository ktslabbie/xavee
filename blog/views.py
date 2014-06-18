from django.views.generic import TemplateView, ListView, DetailView
from .models import Post

class BlogView(TemplateView):
    ''' Simple class-based view to render the post list page. '''
    template_name = "blog/post_list.html"

class PostMixin(object):
    model = Post
     
    def get_queryset(self):
        return self.model.objects.live()
     
    def pre_save(self, obj):
        ''' Force author to current user on save. '''
        obj.author = self.request.user
        return super(PostMixin, self).pre_save(obj)
 
 
class PostListView(PostMixin, ListView):
    pass
 
class PostDetailView(PostMixin, DetailView):
    pass