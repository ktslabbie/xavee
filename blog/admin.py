from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce/tinymce_setup.js',
        ]
    
    fields             = ["published", "title", "slug", "description", "content", "author"]
    list_display       = ["published", "title", "updated_at"]
    list_display_links = ["title"]
    list_editable      = ["published"]
    list_filter        = ["published", "updated_at", "author"]
    search_fields      = ["title", "description", "content"]
    date_hierarchy     = "created_at"

    save_on_top = True
    
    prepopulated_fields = { "slug": ("title",) }

# Register the models here.
admin.site.register(Post, PostAdmin)