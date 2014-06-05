from django.contrib import admin
from .models import Application, AppVersion, Platform, Developer


class VersionInline(admin.TabularInline):
    model = AppVersion
    
    fields =        ["platform", "appstore_link", "release_date"]
    list_display =  ["__unicode__", "appstore_link", "release_date"]
    
    # fields to filter the change list with
    #list_filter = ["clicked_at", "origin", "app_title"]
    
    # fields to search in change list
    search_fields = ["platform", "appstore_link", "release_date"]
    
    # enable the date drill down on change list
    date_hierarchy = "release_date"
    
    # enable the save buttons on top on change form
    # save_on_top = True
    

class AppAdmin(admin.ModelAdmin):
    
    inlines = [ VersionInline, ]
    
    def versions(self):
        html = ""
        for obj in AppVersion.objects.filter(app=self):
            html += '<p>%s (<a href="%s">Appstore link</a>)</p>' %(obj.platform.name, obj.appstore_link)
        return html
    
    versions.allow_tags = True
     
     # Controls what fields show up in the admin creation form
    fields = ["name", "developer", ]
    
    # fields display on change list
    list_display = [ "name", versions, "developer", ]
    
    # fields to filter the change list with
    #list_filter = ["clicked_at", "origin", "app_title"]
    
    # fields to search in change list
    search_fields = ["name", ]
    
    # enable the date drill down on change list
    # date_hierarchy = "release_date"
    
    # enable the save buttons on top on change form
    save_on_top = True
    
    
class DeveloperAdmin(admin.ModelAdmin):
    fields =        ["name", ]
    list_display =  [ "name", ]
    search_fields = ["name", ]
    save_on_top = True
    
class PlatformAdmin(admin.ModelAdmin):
    fields =        ["name", ]
    list_display =  [ "name", ]
    search_fields = ["name", ]
    save_on_top = True

# Register your models here.
admin.site.register(Application, AppAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Developer, DeveloperAdmin)