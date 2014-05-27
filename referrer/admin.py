from django.contrib import admin
from .models import Referral

class ReferralAdmin(admin.ModelAdmin):
    
    # Controls what fields show up in the admin form
    fields = ["origin", "app_title", "destination"]
    
    # fields display on change list
    list_display = ["referral_id", "clicked_at", "origin", "app_title", "click_number"]
    
    #list_display_links = ["id"]
    
    list_editable = []
    
    # fields to filter the change list with
    list_filter = ["clicked_at", "origin", "app_title"]
    
    # fields to search in change list
    search_fields = ["origin", "app_title"]
    
    # enable the date drill down on change list
    date_hierarchy = "clicked_at"
    
    # enable the save buttons on top on change form
    save_on_top = True
    
    #prepopulated_fields = { "slug": ("title",) }

# Register your models here.
admin.site.register(Referral, ReferralAdmin)