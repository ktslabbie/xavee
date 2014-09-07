from django.test import TestCase
from .models import IPhoneVersion, Application, Category, WorldRanking
import tasks
from pprint import pprint
from core import utils
from math import log

# Create your tests here.
class AppCollectionTaskTest(TestCase):
    
    def test_rating_weighting(self):
        
        log_p = 10
        ratings = [ [4.5, 5423], [2.51, 15], [5.0, 6], [3.84, 88576], [1.32, 4532] ]
        total_count = 0.0
        total_count2 = 0.0
        max_count = 0
        
        for rating in ratings:
            
            #print "log(rating): " + str(log10(rating[0]))
            #print "log(rating count): " + str(log(rating[1], log_p))
            #print "weighted rating: " + str(rating[0] * log10(rating[1]))
            
            if rating[1] > max_count:
                max_count = rating[1]
            
            #total_count += log10(rating[0])
            #total_count2 += log10(rating[1])
        
        max_count = float(max_count)
        #print "Max count " + str(max_count)
        
        for rating in ratings:
            #print "Normalized weight: " + str( log10(rating[1]) / max )
            #print "Rating: " + str(rating[0]) + ", rating count: " + str(rating[1])
            #print "Normalized rating: " + str( log(rating[1], 10) * (rating[1] / max_count)   )
            print ""
            print "Rating: " + str(rating[0]) + " (" + str(rating[1]) + ")" 
            brating = (3 * 2.75 + (rating[0] * rating[1])) / (3 + rating[1])
            
            print "Bayesian rating: " + str(brating)
            
        
        #print ""
        #print "Sum log(rating): " + str(total_count)
        #print "Sum log(rating count): " + str(total_count2)
    
    def test_lookup_and_add_ios_app(self):
        ''' Test to make sure looking up and saving apps from the iTunes lookup API works. '''
        appstore_id = 794507331  # Crazy Taxi City Rush by SEGA
        country = 'us'
        application = None
         
        tasks.lookup_and_add_ios_app(appstore_id, country, application)
         
        self.assertTrue(IPhoneVersion.objects.count() == 1)
         
        version = IPhoneVersion.objects.get(appstore_id=appstore_id)
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
         
        fbus = IPhoneVersion.objects.filter(appstore_id=454638411, country='us')
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
