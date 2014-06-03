from django.contrib import admin
from .models import Referral

class ReferralAdmin(admin.ModelAdmin):
    
    # Controls what fields show up in the admin creation form
    fields = ["platform", "name", "medium", "source", "destination"]
    
    # fields display on change list
    list_display = ["referral_link", "referral_id", "platform", "name", "source", "medium", "times_clicked", "created_at"]
    
    #list_display_links = ["id"]
    
    list_editable = []
    
    # fields to filter the change list with
    #list_filter = ["clicked_at", "origin", "app_title"]
    
    # fields to search in change list
    search_fields = ["name", "source", "medium"]
    
    # enable the date drill down on change list
    date_hierarchy = "created_at"
    
    # enable the save buttons on top on change form
    save_on_top = True
    
    #prepopulated_fields = { "slug": ("title",) }

# Register your models here.
admin.site.register(Referral, ReferralAdmin)