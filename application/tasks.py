'''
Created on Jul 30, 2014

This file contains the tasks to retrieve apps from appstores daily.

@author: Kristian
'''
from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger

import json, requests
from unidecode import unidecode
from decimal import Decimal
from django.template import defaultfilters
from .models import Application, IPhoneVersion, Developer, Category, WorldRanking, Ranking
from core import utils, dicts

# Celery logger.
logger = get_task_logger(__name__)

# iTunes domain.
IOS_DOMAIN = 'https://itunes.apple.com/'

# Get a list of the countries we're gathering apps from.
COUNTRIES = dicts.COUNTRY_CHOICES.keys()

# Have a set version as well.
COUNTRY_SET = set(COUNTRIES)

# Initialize a dictionary to store country rankings by app (for generating rank-by-country at the end).
countryrank_by_app = {}

# Initialize the list of world rankings objects to insert to DB.
# This will be a list of dictionaries with country and a ranking dictionary. 
world_rankings = { k:[] for k in COUNTRIES }

@shared_task
def collect_all_ios_rankings(limit):
    #for cat_id in [0] + range(6000, 6019) + range(6020, 6024) + range(7001, 7010) + range(7011, 7020):
    for cat_id in [0] + [6014]:
        collect_ios_ranking(dicts.TOP_FREE, cat_id, limit)
        collect_ios_ranking(dicts.TOP_PAID, cat_id, limit)
        collect_ios_ranking(dicts.TOP_GROSSING, cat_id, limit)

@shared_task
def collect_ios_ranking(ranking_type, ranking_category_id, limit):
    '''
    Task to collect iOS rankings for all countries registered in the model.
    Input: the ranking type int, category ID (<= 0 for unspecified), and max results to return (max 200).
    Output: The new ranking at the date of execution added to DB.
    '''
    
    # Retrieve the string to insert into the RSS URL.
    type_string = dicts.ITUNES_TYPESTRINGS.get(ranking_type)
    
    # Get the category with the given ID, or None if it doesn't exist.
    category = Category.objects.filter(id=ranking_category_id).first()
    
    # Check if category is valid. 0 or lower means get all categories (iTunes defaults to this for invalid numbers).
    # TODO: combined categories
    if ranking_category_id <= 0 or category is not None:
#         if ranking_category_id is 7006:
#             path = '/rss/' + type_string + '/limit=' + str(limit) + '/genre=7006-7007/json'
#         else:
        path = '/rss/' + type_string + '/limit=' + str(limit) + '/genre=' + str(ranking_category_id) + '/json'
    else:
        print("Invalid category!")
        return
    
    print("Calling " + path + "...")
    
    # Iterate over the countries and collect rankings for each.
    for country in COUNTRIES:
        collect_ios_ranking_for_country(path, ranking_type, category, country)
    
    # Add the app rankings for foreign countries to each country ranking.
    add_apprank_by_country(ranking_type, category)
    
    # Re-initialize the ranking objects.
    global countryrank_by_app, world_rankings
    countryrank_by_app = {}
    world_rankings = { k:[] for k in COUNTRIES }
    
    print("All apps collected and ranked.")


def collect_ios_ranking_for_country(path, ranking_type, category, country):
    ''' Sub-function to collect a type of ranking for one country. '''
    
    # First call the appropriate RSS feed (list of top {limit} apps).
    rss_url = IOS_DOMAIN + country + path
    print("Retrieving " + rss_url + "...")
    
    # Get the JSON. Retry at least 40 times in case of a connection error, waiting longer each before each new try.
    for retry in utils.retryloop(40, timeout=120, delay=1, backoff=2):
        try:
            rss_resp = requests.get(rss_url)
            list_data = json.loads(rss_resp.text)
        except Exception:
            print("Connection failed. Retrying...")
            retry()
            
    if not 'entry' in list_data['feed']:
        print "No ranking found!"
        return
    
    # Initialize the ranking and the rankings list for this country.
    rankings = []
    rank_counter = 1
    
    # Iterate over the apps in the JSON list retrieved.
    for app in list_data['feed']['entry']:
        appstore_id = app['id']['attributes']['im:id']
        
        print("Processing the #" + str(rank_counter) + " app '" + app['im:name']['label'] + "' in country '" + country + "'...")
        
        # TODO: Check if the application already exists here (for a fast mode?).
        version = None
        
        # Check if we already have this Version of this app for this country in the DB.
        version = IPhoneVersion.objects.filter(appstore_id=appstore_id, country=country).first()
        
        if not version:
            
            # The Version with this ID does not yet exist for this country.
            # There may be versions for other countries already. Check.
            versions = IPhoneVersion.objects.filter(appstore_id=appstore_id)
            
            # Initialize a country list.
            countries = COUNTRIES[:]
            
            # Remove countries whose versions are already in the DB.
            for ver in versions:
                if ver.country in countries:
                    countries.remove(ver.country)
            
            # Lookup versions for all remaining countries.
            for version_country in countries:
                if version is not None:
                    lookup_and_add_ios_app(appstore_id, version_country, version.application)
                else:
                    version = lookup_and_add_ios_app(appstore_id, version_country, None)
            
            # Shouldn't happen but does sometimes. iTunes error. Just skip if None.
            if version is None:
                continue
                
            # Get the world average rating and total rating count by averaging over all versions.
            compute_itunes_world_rating(version.application)
            
            # Finally, assure we have the version of the current country.
            version = IPhoneVersion.objects.get(appstore_id=appstore_id, country=country)
        # endif
        
        # We should have a version now.
        assert(version is not None)
        
        if category.id == 0 or category.id == 6014:
            # Create the new ranking (only all apps and all games) for this version and add it to the list (we save to DB in bulk later).
            rankings.append(Ranking(version=version, ranking_type=ranking_type, category=category, rank=rank_counter))
        
        # Also add the rank to a dictionary we will use later to add foreign rankings to apps.
        countryrank_by_app.setdefault(version.application.id, {})[country] = rank_counter
        
        # Add the app info to the world rankings dictionary (will be converted to JSON later).
        world_rankings.get(country).append({ 
            'id': version.id,
            'application': {
                'id': version.application.id,
                'title': version.application.title,
                'slug': version.application.slug,
                'developer': {
                    'id': version.application.developer.id,
                    'name': version.application.developer.name,
                    'slug': version.application.developer.slug,
                },
                'img_small': version.application.img_small,
                'itunes_world_rating': version.application.itunes_world_rating,
                'itunes_world_rating_count': version.application.itunes_world_rating_count,
            },
            'appstore_id': version.appstore_id,
            'price': version.price,
            'rating': {
#                 'current_version_rating': version.current_version_rating,
#                 'current_version_count': version.current_version_count,
                'overall_rating': version.overall_rating,
                'overall_count': version.overall_count,
            },
            'foreign_ranking': {}, # This will contain rankings for this app in other countries.
        })
        
        # Increment the rank counter.
        rank_counter += 1
    
    if category.id == 0 or category.id == 6014:
        # Collected all rankings. Remove the previous ranking and add the new ones.
        Ranking.objects.filter(ranking_type=ranking_type, category=category, version__country=country).delete()
        Ranking.objects.bulk_create(rankings)

def lookup_and_add_ios_app(appstore_id, version_country, application):
    '''
    This function queries app details for the current country using the lookup API, 
    and creates an application/version where none exist yet. 
    '''
    
    lookup_url = IOS_DOMAIN + 'lookup?id=' + str(appstore_id) + '&country=' + version_country
    
    print("Calling " + lookup_url + "... ")
    
    for retry in utils.retryloop(40, timeout=120, delay=1, backoff=2):
        try:
            lookup_resp = requests.get(lookup_url)
            detail_data = json.loads(lookup_resp.text)
        except Exception:
            print("Connection failed. Retrying...")
            retry()
    
    # Check if we found something. No results means this app isn't being sold in this country.
    if detail_data['resultCount'] == 0:
        print("No result found for " + version_country + ".")
    
    else:
        # Found an app. Get the details. There will always be only one result.
        print("Found an app for " + version_country + "!")
        
        app_detail = detail_data['results'][0]        
        title = app_detail['trackName']
        img_small = app_detail['artworkUrl60']
        
        # There are some apps without an artist URL. Slugify the name for these ourselves, rather than getting it from the URL.
        dev_slug = ''
        if 'artistViewUrl' in app_detail:
            dev_slug = utils.get_slug_from_itunes_url(app_detail['artistViewUrl'])
        else:
            dev_slug = defaultfilters.slugify(unidecode(app_detail['artistName']))
            
        app_slug = utils.get_slug_from_itunes_url(app_detail['trackViewUrl'])
        
        # Have we already added the Application of which this is a Version?
        if application is None:
            
            # Nope. First get the developer, creating one if needed.
            developer = Developer.objects.filter(ios_id=app_detail['artistId']).first()
            if developer is None:
                developer = Developer(ios_id=app_detail['artistId'], name=app_detail['artistName'], slug=dev_slug)
                developer.save()
            
            # We have enough to create and save an Application.
            application = Application(title=title, slug=app_slug, developer=developer, img_small=img_small)
            application.save()
            
            # Next get the categories.
            genre_ids = app_detail['genreIds']
            genres = app_detail['genres']
            
            # An Application can have several categories, so check all of them.
            for i in range(len(genre_ids)):
                category, created = Category.objects.get_or_create(id=genre_ids[i])
                
                if created:
                    # Unseen category. Better add the name too.
                    # There's a chance this isn't in English. Check manually later.
                    category.name = genres[i]
                    category.save()
                
                # Add the category to the application ManyToMany field.
                application.categories.add(category)
            
            # Save the application again.
            application.save()
        
        # We should have an application now.
        assert(application is not None)
        
        # Get the remaining Version-specific data.
        bundle_id = app_detail['bundleId']
        price = app_detail['price']
        currency = app_detail['currency']
        release_date = app_detail['releaseDate']
        
        # Get the ratings for this version (if it has ratings; new games may not have them yet).
        current_version_rating = None
        current_version_count = None
        overall_rating = None
        overall_count = None
        
        if 'averageUserRatingForCurrentVersion' in app_detail and 'userRatingCountForCurrentVersion' in app_detail:
            current_version_rating = app_detail['averageUserRatingForCurrentVersion']
            current_version_count = app_detail['userRatingCountForCurrentVersion']
    
        if 'averageUserRating' in app_detail and 'userRatingCount' in app_detail:
            overall_rating = app_detail['averageUserRating']
            overall_count = app_detail['userRatingCount']
        
        # Build the IPhoneVersion object and save to DB.
        version, created = IPhoneVersion.objects.get_or_create(country=version_country, title=title, application=application, appstore_id=appstore_id,
                          bundle_id=bundle_id, price=price, currency=currency, release_date=release_date, current_version_rating=current_version_rating,
                          current_version_count=current_version_count, overall_rating=overall_rating, overall_count=overall_count)
        
        return version

def add_apprank_by_country(ranking_type, category):
    ''' Add world rankings for each app to each app in the rankings for each country. '''
    
    for country in COUNTRIES:
        country_ranking = world_rankings.get(country)
        
        for app in country_ranking:
            foreign_dict = countryrank_by_app.get(app['application']['id'])
            
            for foreign_country in foreign_dict.keys():
                if foreign_country is not country:
                    app['foreign_ranking'][foreign_country] = foreign_dict.get(foreign_country)
        
        WorldRanking.objects.filter(ranking_type=ranking_type, category=category, platform=dicts.IPHONE, country=country).delete()
        world_ranking = WorldRanking(ranking_type=ranking_type, category=category, platform=dicts.IPHONE, 
                                     country=country, currency=dicts.CURRENCIES.get(country), ranking=country_ranking)
        world_ranking.save()

def compute_all_itunes_world_ratings():
    for application in Application.objects.all():        
        compute_itunes_world_rating(application)

def compute_itunes_world_rating(application):
    
    rating_sum = 0.0
    rating_count = 0
    
    for version in IPhoneVersion.objects.filter(application=application):
        if version.overall_rating is not None and version.overall_count is not None:
            rating_sum += float(version.overall_rating) * version.overall_count
            rating_count += version.overall_count
    
    if rating_count is not 0:
        rating_avg = round(rating_sum / rating_count, 2)
    else:
        rating_avg = None
 
    application.itunes_world_rating = rating_avg
    application.itunes_world_rating_count = rating_count
    application.save()

def make_application_titles():
    pass

def get_japanese_app_ids():
    out_str = ''
    results = []
    # ((50 * 2.75 + (app.application.itunes_world_rating * app.application.itunes_world_rating_count)) / (50 + app.application.itunes_world_rating_count)).toFixed(2)
    for version in IPhoneVersion.objects.filter(country='jp', application__itunes_world_rating__gte=4).order_by('-application__itunes_world_rating'):
        #print u"Processing " + version.appstore_id + " (rating: " + version.application.itunes_world_rating + ")..."
        #appstore_ids += '' + str(version.appstore_id) + '\t' + str(version.release_date) + '\n'
        rating = version.application.itunes_world_rating
        rating_count = version.application.itunes_world_rating_count
        
        bayesian = (1000 * Decimal(2.75) + (rating * rating_count)) / (1000 + rating_count)
        
        
        results.append((version.appstore_id, round(bayesian, 2), rating_count))
    
    sorted_by_bayesian = sorted(results, key=lambda tup: tup[1], reverse=True)
    
    for tup in sorted_by_bayesian:
        out_str += str(tup[0]) + ',' + str(tup[1])  + ',' + str(tup[2])  + '\n'
    
    f = open('japanese.apps.txt','w')    
    f.write(out_str)
    f.close()
        

# def compare_app_versions():
#      
#     developers = Developer.objects.all()
#      
#     for developer in developers:
#         
#         print "Checking developer " + developer.name + "..."
#         
#         applications = list(Application.objects.filter(developer=developer))
#         all_countries = []
#         
#         for i in range (0, len(applications)):
#             
#             versions = list(IPhoneVersion.objects.filter(application=applications[i]))
#             countries = []  
#             
#             for j in range (0, len(versions)):
#                 countries.append(versions[j].country)
#             
#             # Ex: [ ['us', 'jp'], ['us', 'jp', 'gb']  ]
#             all_countries.append(countries)
#           
#         
#           
#         for i in range(0, len(all_countries)-1):
#             for k in range(i+1, len(all_countries)-1):
#                 combined = set(all_countries[i]) & set(all_countries[k])
#                 if not combined:
#                     # Compare categories
#                     app_a_categories = applications[i].categories.all()
#                     app_b_categories = applications[k].categories.all()
#                     
#                     a_set1 = set()
#                     b_set1 = set()
#                     
#                     for category in app_a_categories:                        
#                         a_set1.add(category.id)
#                     for category in app_b_categories:
#                         b_set1.add(category.id)
#                     ab_set1 = a_set1 & b_set1
#                     
#                     version_a = IPhoneVersion.objects.filter(application=applications[i])[0]
#                     version_b = IPhoneVersion.objects.filter(application=applications[k])[0]
#                     
#                     bundle_a_split = version_a.bundle_id.split(".")[:-1]
#                     bundle_b_split = version_b.bundle_id.split(".")[:-1]
#                     
#                     print version_a.bundle_id + " -> " + ''.join(bundle_a_split)
#                     print version_b.bundle_id + " -> " + ''.join(bundle_b_split)
#                     
#                     
#                     
#                     if len(ab_set1) is len(a_set1) and ''.join(bundle_a_split) is ''.join(bundle_b_split): #and applications[i].title == applications[k].title:
#                         prompt = "> "
#                         print "Match? " + applications[i].title + " and " + applications[k].title + " are similar."
#                         
#                         print ""
#                         print "Application comparison:"
#                         print "Title: " + applications[i].title + " and " + applications[k].title
#                         print "Slug: " + applications[i].slug + " and " + applications[k].slug
#                         print "Icon URL: " + applications[i].img_small + " and " + applications[k].img_small
#                         #print "Categories: " + list(applications[i].categories.all()) + " and " + list(applications[k].categories.all())
#                         
#                         print ""
#                         print "Version comparison:"
#                         version_a = IPhoneVersion.objects.filter(application=applications[i])[0]
#                         version_b = IPhoneVersion.objects.filter(application=applications[k])[0]
#                         print "Country: " + version_a.country + " and " + version_b.country
#                         print "Local title: " + version_a.title + " and " + version_b.title
#                         print "Appstore_id: " + str(version_a.appstore_id) + " and " + str(version_b.appstore_id)
#                         print "Bundle_id: " + version_a.bundle_id + " and " + version_b.bundle_id
#                         print "Price/currency: " + str(version_a.price) + " " + version_a.currency + " and " + str(version_b.price) + " " + version_b.currency
#                         print "Release date: " + str(version_a.release_date) + " and " + str(version_b.release_date)
#                         print "iTunes rating: " + str(version_a.itunes_rating.overall_rating) + " and " + str(version_b.itunes_rating.overall_rating)
#                         print "iTunes rating count: " + str(version_a.itunes_rating.overall_count) + " and " + str(version_b.itunes_rating.overall_count)
#                         
#                         print "Combine? Y/N?"
#                         answer = raw_input(prompt)
#                         if answer is "y" or answer is "Y":
#                             a_versions = IPhoneVersion.objects.filter(application=applications[i])
#                             
#                             
#                             for version in a_versions:
#                                 version.application = applications[k]
#                                 version.save()
#                                 
#                             for category in app_a_categories:
#                                 applications[i].categories.remove(category)
#                                 
#                             applications[i].delete()
#                             
#                             break
                            
