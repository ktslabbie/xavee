from django.test import TestCase
from .models import Version, Ranking, Application, Category, WorldRanking
import tasks
from pprint import pprint
from core import utils

# Create your tests here.
class AppCollectionTaskTest(TestCase):
    
    def test_lookup_and_add_ios_app(self):
        ''' Test to make sure looking up and saving apps from the iTunes lookup API works. '''
        appstore_id = 794507331  # Crazy Taxi City Rush by SEGA
        country = 'us'
        application = None
        
        tasks.lookup_and_add_ios_app(appstore_id, country, application)
        
        self.assertTrue(Version.objects.count() == 1)
        
        version = Version.objects.get(appstore_id=appstore_id)
        self.assertEqual(version.bundle_id, "com.sega.cityrush")
        self.assertEqual(version.application.developer.name, "SEGA")
        self.assertEqual(version.application.developer.slug, "sega")
        self.assertEqual(version.application.slug, "crazy-taxi-city-rush")
        
        rating = version.itunes_rating
        self.assertEqual(rating.overall_rating, 4.5)
    
    def test_collect_ios_ranking(self):
        
        category = Category(id=6014, name="Games")
        category.save()
        
        #type_int = 1
        tasks.lookup_and_add_ios_app(454638411, 'us', None)
        
#         tasks.collect_ios_ranking(type_int, 6014, 2)
#          
#         self.assertTrue(Version.objects.count() > 10)
#         
#         for wr in WorldRanking.objects.all():
#             print("WR Country: " + wr.country)
#             print("JSON:")
#             pprint(wr.ranking)
#          
#         for app in Application.objects.all():
#             print("App: " + app.title)
#             print("Slug: " + app.slug)
#             print("ID: " + str(app.pk))
#             print("Versions: ")
#             for ver in Version.objects.filter(application=app):
#                 print("    Country: " + ver.country)
#                 print("    Appstore ID: " + str(ver.appstore_id))
#                 print("    Bundle ID: " + ver.bundle_id)
        
        
        
        app = Application.objects.get(slug="facebook-messenger")
        self.assertEqual(app.title, "Facebook Messenger")
        
        fbus = Version.objects.filter(appstore_id=454638411, country='us')
        self.assertTrue(len(fbus) == 1, "Length is " + str(len(fbus)))
        
        
        #version = Version.objects.get(appstore_id=736683061, country=country)
        #self.assertEqual(version.bundle_id, "com.doublespeakgames-scratchworkdev.adarkroom")
        #self.assertEqual(version.application.title, "A Dark Room")
    
        
    ''' test_collect_ios_ranking automatically tests this as well. Removed to save needless HTTP requests. '''    
    #     def test_collect_ios_ranking_for_country(self):
    #         
    #         country = 'us'
    #         platform = tasks.IOS_PLATFORM
    #         ranking_type = Ranking.TOP_FREE
    #         path = '/rss/topfreeapplications/limit=3/json'
    #         
    #         tasks.collect_ios_ranking_for_country(path, ranking_type, platform, country)
    #         
    #         self.assertTrue(Version.objects.count() > 20)
            
    #version = Version.objects.get(appstore_id=736683061, country=country)
    #self.assertEqual(version.bundle_id, "com.doublespeakgames-scratchworkdev.adarkroom")
    #self.assertEqual(version.application.title, "A Dark Room")
