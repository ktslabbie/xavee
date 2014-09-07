from django.contrib import admin
from .models import Referral

class ReferralAdmin(admin.ModelAdmin):
    
    fields         = ["referral_name", "source", "medium", "destination"]
    list_display   = ["referral_id", "referral_name", "referral_link", "source", "medium", "times_clicked", "destination", "created_at"]
    search_fields  = ["source", "medium"]
    date_hierarchy = "created_at"
    
    save_on_top = True

# Register the models here.
admin.site.register(Referral, ReferralAdmin)