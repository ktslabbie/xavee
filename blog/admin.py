from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce/tinymce_setup.js',
        ]
    
    # Controls what fields show up in the admin form
    fields = ["published", "title", "slug", "description", "content", "author"]
    
    # fields display on change list
    list_display = ["published", "title", "updated_at"]
    
    list_display_links = ["title"]
    
    list_editable = ["published"]
    
    # fields to filter the change list with
    list_filter = ["published", "updated_at", "author"]
    
    # fields to search in change list
    search_fields = ["title", "description", "content"]
    
    # enable the date drill down on change list
    date_hierarchy = "created_at"
    
    # enable the save buttons on top on change form
    save_on_top = True
    
    prepopulated_fields = { "slug": ("title",) }

# Register your models here.
admin.site.register(Post, PostAdmin)