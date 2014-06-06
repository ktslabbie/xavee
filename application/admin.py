from django.contrib import admin
from .models import Application, Version, Platform, Developer

class VersionInline(admin.TabularInline):
    model = Version
    
    fields         = ["platform", "appstore_link", "release_date"]
    list_display   = ["__unicode__", "appstore_link", "release_date"]
    search_fields  = ["platform", "appstore_link", "release_date"]
    date_hierarchy = "release_date" 

class AppAdmin(admin.ModelAdmin):
    
    def versions(self):
        html = ""
        for obj in Version.objects.filter(app=self):
            html += '<p>%s (<a href="%s">Appstore link</a>)</p>' %(obj.platform.name, obj.appstore_link)
        return html
    
    versions.allow_tags = True
    
    inlines = [ VersionInline, ]

    fields         = [ "name", "developer", ]
    list_display   = [ "name", versions, "developer", "date_added" ]
    list_filter    = [ "name", "developer" ]
    search_fields  = [ "name", ]
    date_hierarchy = "date_added"
    save_on_top    = True
    
class DeveloperAdmin(admin.ModelAdmin):
    fields         = ["name", ]
    list_display   = [ "name", ]
    search_fields  = ["name", ]
    save_on_top    = True
    
class PlatformAdmin(admin.ModelAdmin):
    fields         = ["name", ]
    list_display   = [ "name", ]
    search_fields  = ["name", ]
    save_on_top    = True

# Register your models here.
admin.site.register(Application, AppAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Developer, DeveloperAdmin)