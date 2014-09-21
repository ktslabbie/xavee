from django.contrib import admin
from .models import Application, IPhoneVersion, Developer, Category
from modeltranslation.admin import TranslationAdmin

class IPhoneVersionInline(admin.TabularInline):
    model = IPhoneVersion
    
    fields         = ["country", "title", "application", "appstore_id", "bundle_id", "price", "currency", "release_date", ]
    list_display   = ["__unicode__", "country", "bundle_id", "price", "currency", "release_date", "created_at", "updated_at", ]
    search_fields  = ["country", "title", "application", "platform", "bundle_id", "price", "currency", "release_date", ]
    date_hierarchy = "release_date"

class ApplicationAdmin(admin.ModelAdmin):
    
    def categories(self):
        return ", ".join([c.name for c in self.categories.all()])
    
    def versions(self):
        ver = IPhoneVersion.objects.filter(application=self).first()
        html = '<a href="https://itunes.apple.com/us/app/id%s">iPhone</a>' % (ver.appstore_id)
#         for obj in Version.objects.filter(application=self):
#             #rank = "n/a"
#             query_set = Ranking.objects.filter(version=obj)
#             if len(query_set) > 0:
#                 rank = query_set.latest("since").rank
#                 html += '<p>%s: %s</p>' % (dicts.COUNTRY_CHOICES.get(obj.country), rank)
        return html
    
    versions.allow_tags = True
    
    inlines = [ IPhoneVersionInline, ]

    fields         = [ "title", "slug", "developer", "categories", ]
    list_display   = [ "title", versions, "developer", categories, "created_at", "updated_at" ]
    list_filter    = [ "title", "developer" ]
    search_fields  = [ "title", ]
    date_hierarchy = "created_at"
    save_on_top    = True
    
class DeveloperAdmin(admin.ModelAdmin):
    fields         = ["ios_id", "android_id", "name", ]
    list_display   = ["ios_id", "name", ]
    search_fields  = ["ios_id", "name", ]
    save_on_top    = True
    
class CategoryAdmin(TranslationAdmin):
    fields         = ["id", "name", ]
    list_display   = ["id", "name_en", "name_ja", ]
    search_fields  = ["id", "name_en", "name_ja", ]
    save_on_top    = True
    
class RankingAdmin(admin.ModelAdmin):
    fields         = ["ranking_type", "rank"]
    list_display   = ["version", "ranking_type", "since", "rank"]
    search_fields  = ["ranking_type", ]
    save_on_top    = True

# Register models here to make them visible in the Admin panel.
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Category, CategoryAdmin)