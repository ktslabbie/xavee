from django.contrib import admin
from .models import Referral

class ReferralAdmin(admin.ModelAdmin):
    
    fields         = ["app", "source", "medium"]
    list_display   = ["referral_link", "app", "source", "medium", "times_clicked", "created_at"]
    search_fields  = ["app", "source", "medium"]
    date_hierarchy = "created_at"
    
    save_on_top = True

# Register the models here.
admin.site.register(Referral, ReferralAdmin)