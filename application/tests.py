"""
Created on Jul 30, 2014

Tests for application.

@author: Kristian
"""
from django.test import TestCase
from .models import IPhoneVersion, Application, Developer
from .rating_utils import XaveeScore
import tasks
from datetime import datetime

# Create your tests here.
class AppCollectionTaskTest(TestCase):
    
    fixtures = ['application',]
    
    def setUp(self):
        TestCase.setUp(self)
    
    def test_appplication_model(self):
        self.assertIsNotNone(Application.objects.first())                       # Simple fixture load test.
        
        clashUS = IPhoneVersion.objects.get(title="Clash of Clans", country="us")
        self.assertIsNotNone(clashUS)                                           # Clash of Clans (US) exists?
        self.assertEqual(clashUS.appstore_id, 529479190)                        # The right appstore ID?
        self.assertEqual(clashUS.bundle_id, "com.supercell.magic")              # The right bundle ID?
        self.assertEqual(clashUS.currency, "USD")                               # The right currency?
        self.assertGreaterEqual(clashUS.overall_count, 1024557)                 # Overall rating count at least 1024557? (can never decrease)
        self.assertEqual(clashUS.release_date, datetime(2012, 8, 2, 17, 24, 58))# The right release date?
        
        clashApp = clashUS.application
        self.assertEqual(clashApp.title, "Clash of Clans")                      # The right universal title?
        self.assertEqual(clashApp.slug, "clash-of-clans")                       # The right slug?
        self.assertGreaterEqual(clashApp.itunes_world_rating_count, 2502221)    # Overall rating count at least 2502221? (can never decrease)
        self.assertFalse(clashApp.multi_build)                                  # Clash of Clans is not a multi-build app
        self.assertGreaterEqual(clashApp.itunes_world_rating, 1.0)              # iTunes world rating must be between 1.0 and 5.0
        self.assertLessEqual(clashApp.itunes_world_rating, 5.0)                 # iTunes world rating must be between 1.0 and 5.0
        self.assertGreaterEqual(clashApp.xavee_score, 0)                        # Xavee rating must be between 0 and 100
        self.assertLessEqual(clashApp.xavee_score, 100)                         # Xavee rating must be between 0 and 100
        
        clashDev = clashApp.developer
        self.assertEqual(clashDev.ios_id, 488106216)                            # The right iOS ID for this developer?
        self.assertEqual(clashDev.name, "Supercell")                            # The right developer name?
        self.assertEqual(clashDev.slug, "supercell")                            # The right slug?
        
        catIDList = [cat.id for cat in clashApp.categories.all()]
        catNameList = [cat.name for cat in clashApp.categories.all()]
        
        self.assertIn("Action", catNameList)                                    # Is Action contained in the categories?
        self.assertIn(6014, catIDList)                                          # Is the ID for 'Games' contained?

    def test_slugification(self):
        sameNameDev = Developer(name=u"SuPeRCeLl", ios_id=666666)               # Make a developer generating a slug that already exists.
        sameNameDev.save()
        self.assertEqual(sameNameDev.slug, "supercell-1")                       # Was the -1 appended correctly?
        
        sameNameDev2 = Developer(name=u"SuperCeLl", ios_id=666667)              # Make another developer generating a slug that already exists.
        sameNameDev2.save()
        self.assertEqual(sameNameDev2.slug, "supercell-2")                      # Was the -2 appended correctly?
        
        app2 = Application(title=u"CLasH oF ClAns", developer=sameNameDev2, price=0)     # Test the same for Application as well.
        app2.save()
        self.assertEqual(app2.slug, "clash-of-clans-1")                         # Was the -1 appended correctly?
        
    def test_update_app_ratings(self):
        score = XaveeScore()
        score.set_bayesian_params(2.75, 200)
        b = score.get_xavee_score(5, 200)
        print "Xavee score of 5 and 200 = " + str(b)
        self.assertEqual(b, 72)
        print "What if the number of ratings is 0?"
        b = score.get_xavee_score(None, 0)
        print "It's " + str(b) + "."
        self.assertEqual(b, 50)
        self.assertEqual(score.get_xavee_score(1.00, 9999999), 0)               # Boundary test: at least 0
        self.assertEqual(score.get_xavee_score(5.00, 9999999), 100)             # Boundary test: at most 100
        
        print "Testing Xavee rating update..."
        tasks.update_app_ratings()
        for app in Application.objects.all():
            print "" + app.title + " - R: " + str(app.itunes_world_rating) + ", C: " + str(app.itunes_world_rating_count) + ", X: " + str(app.xavee_score)
            self.assertTrue(app.xavee_score > 0)
    
    def test_update_dev_ratings(self):
        score = XaveeScore()
        score.set_bayesian_params(2.75, 0.5)
        b = score.get_xavee_average(500, 5)
        print "Xavee developer score of 294 total and 5 apps = " + str(b)
        #self.assertEqual(b, 72)
        
        print "Testing Xavee rating update..."
        tasks.update_dev_ratings()
        for dev in Developer.objects.all():
            for app in Application.objects.filter(developer__ios_id=dev.ios_id):
                print "App for " + dev.name + ": " + app.title + ", X: " + str(app.xavee_score)
                
            print "" + dev.name + " X: " + str(dev.xavee_score)
            self.assertTrue(dev.xavee_score > 0)
            
    def test_update_apps_from_versions(self):
        clashUS = IPhoneVersion.objects.get(title="Clash of Clans", country="us")
        clashUS.price = 499
        clashUS.currency = "JPY"
        clashUS.save()
        
        print "Testing app update from versions..."
        tasks.update_apps_from_versions()
        app = Application.objects.get(title="Clash of Clans")
        
        print "" + app.title + " - Price: " + str(app.currency) + str(app.price)
        self.assertEqual(app.price, 499)
        self.assertEqual(app.currency, "JPY")
    
    def test_app_creation(self):
        ''' Test to make sure looking up and saving apps from the iTunes lookup API works. '''
        appstore_id = 454638411  # Facebook Messenger (should not exist in game-only DB)
        country = 'us'
        application = None

        tasks.lookup_and_add_ios_app(appstore_id, country, application)
         
        version = IPhoneVersion.objects.get(appstore_id=appstore_id)
        self.assertEqual(version.bundle_id, "com.facebook.Messenger")
        self.assertEqual(version.application.developer.name, "Facebook, Inc.")
        self.assertEqual(version.application.developer.slug, "facebook-inc.")
        self.assertEqual(version.application.slug, "facebook-messenger")

        appstore_id = 651510680
        country = 'es'
        
        tasks.create_and_add_application(appstore_id, country)
        
        version = IPhoneVersion.objects.get(appstore_id=appstore_id, country=country)
        self.assertEqual(version.application.developer.name, "Etermax")
        self.assertEqual(version.title, "Preguntados")
        self.assertEqual(version.application.title, "Trivia Crack")             # Make sure the application gets the US title.
        
        version.application.title = "Preguntados"
        version.application.save()
        
        version = IPhoneVersion.objects.get(appstore_id=appstore_id, country=country)
        self.assertEqual(version.application.title, "Preguntados")             # We changed it back to the Spanish title.
        
        tasks.update_apps_from_versions()
        
        version = IPhoneVersion.objects.get(appstore_id=appstore_id, country=country)
        self.assertEqual(version.application.title, "Trivia Crack")             # Make sure the application gets the US title again.

#      
#     def test_collect_ios_ranking(self):
#          
#         category = Category(id=6014, name="Games")
#         category.save()
#          
#         #type_int = 1
#         tasks.lookup_and_add_ios_app(454638411, 'us', None)
         
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
         
         
#          
#         app = Application.objects.get(slug="facebook-messenger")
#         self.assertEqual(app.title, "Facebook Messenger")
#          
#         fbus = IPhoneVersion.objects.filter(appstore_id=454638411, country='us')
#         self.assertTrue(len(fbus) == 1, "Length is " + str(len(fbus)))
         
         
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
