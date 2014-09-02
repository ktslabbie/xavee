'''
Created on Jul 30, 2014

This file contains the tasks to retrieve apps from appstores daily.

@author: Kristian
'''
from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from pprint import pprint

import json, requests
from unidecode import unidecode
from django.template import defaultfilters
from .models import Application, Ranking, Version, Developer, Category, ITunesRating, WorldRanking
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
    for cat_id in [-1] + range(6000, 6019) + range(6020, 6023) + range(7001, 7020):
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
    if ranking_category_id <= 0 or category is not None:
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
    
    # Initialize the ranking and the rankings list for this country.
    rank_counter = 1
    rankings = []
    
    # Iterate over the apps in the JSON list retrieved.
    for app in list_data['feed']['entry']:
        appstore_id = app['id']['attributes']['im:id']
        
        print("Processing the #" + str(rank_counter) + " app '" + app['im:name']['label'] + "' in country '" + country + "'...")
        
        # Check if we already have this Version of this app for this country in the DB.
        version = Version.objects.filter(appstore_id=appstore_id, country=country).first()
        
        if not version:
            
            # The Version with this ID does not yet exist for this country. Let's create one.
            versions = Version.objects.filter(appstore_id=appstore_id)
            version = lookup_and_add_ios_app(appstore_id, country, None)
            
            # Initialize a country list and remove the current one.
            countries = COUNTRIES[:]
            countries.remove(country)
            
            # Also remove countries whose versions are already in the DB.
            for ver in versions:
                if ver.country in countries:
                    countries.remove(ver.country)
            
            # Lookup apps for all remaining countries.
            for version_country in countries:
                lookup_and_add_ios_app(appstore_id, version_country, version.application)
            
        # endif
        
        # We should have a version now.
        assert(version is not None)
        
        # Time to create the new ranking for this version and add it to the list (we save to DB in bulk later).
        # rankings.append(Ranking(version=version, ranking_type=ranking_type, category=category, rank=rank_counter))
        
        # Also add the rank to a dictionary we will use later to add foreign rankings to apps.
        countryrank_by_app.setdefault(version.application.id, {})[country] = rank_counter
        
        # In case some broken Version objects remain in DB.
        try:
            getattr(version, 'itunes_rating')
        except ITunesRating.DoesNotExist:
            print("Rating does not exist! Just collect the version again.")
            version = lookup_and_add_ios_app(appstore_id, country, version.application)
        
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
            },
            'appstore_id': version.appstore_id,
            'price': version.price,
            'currency': version.currency,
            'rating': {
                'current_version_rating': version.itunes_rating.current_version_rating,
                'current_version_count': version.itunes_rating.current_version_count,
                'overall_rating': version.itunes_rating.overall_rating,
                'overall_count': version.itunes_rating.overall_count,
            },
            'foreign_ranking': {}, # This will contain rankings for this app in other countries.
        })
        
        # Increment the rank counter.
        rank_counter += 1
    
    # Collected all rankings. Remove the previous ranking and add the new ones.
    # Ranking.objects.filter(ranking_type=ranking_type, version__country=country).delete()
    # Ranking.objects.bulk_create(rankings)

def lookup_and_add_ios_app(appstore_id, version_country, application):
    '''
    This function queries app details for the current country using the lookup API, 
    and creates an application/version where none exist yet. 
    '''
    
    lookup_url = IOS_DOMAIN + 'lookup?id=' + str(appstore_id) + '&country=' + version_country
    
    print("Calling " + lookup_url + "...")
    
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
        print("Found an app for " + version_country + "!...")
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
        
        # Build the Version object and save to DB.
        version = Version(country=version_country, title=title, application=application, platform=dicts.IPHONE, appstore_id=appstore_id,
                          bundle_id=bundle_id, price=price, currency=currency, release_date=release_date)
        version.save()
        
        # Get the ratings for this version (if it has ratings; new games may not have them yet).
        current_version_rating = None
        current_version_count = None
        overall_rating = None
        overall_count = None
        
        try:
            if 'averageUserRatingForCurrentVersion' in app_detail and 'userRatingCountForCurrentVersion' in app_detail:
                current_version_rating = app_detail['averageUserRatingForCurrentVersion']
                current_version_count = app_detail['userRatingCountForCurrentVersion']
        
            if 'averageUserRating' in app_detail and 'userRatingCount' in app_detail:
                overall_rating = app_detail['averageUserRating']
                overall_count = app_detail['userRatingCount']
        except KeyError:
            print("Key error!")
        
        # Build the ITunesRating object and save to DB.
        rating = ITunesRating(version=version, current_version_rating=current_version_rating, current_version_count=current_version_count,
                              overall_rating=overall_rating, overall_count=overall_count)
        rating.save()
        
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
        world_ranking = WorldRanking(ranking_type=ranking_type, category=category, platform=dicts.IPHONE, country=country, ranking=country_ranking)
        world_ranking.save()


def compare_app_versions():
     
    developers = Developer.objects.all()
     
    for developer in developers:
        
        print "Checking developer " + developer.name + "..."
        
        applications = list(Application.objects.filter(developer=developer))
        all_countries = []
        
        for i in range (0, len(applications)):
            
            versions = list(Version.objects.filter(application=applications[i]))
            countries = []  
            
            for j in range (0, len(versions)):
                countries.append(versions[j].country)
            
            # Ex: [ ['us', 'jp'], ['us', 'jp', 'gb']  ]
            all_countries.append(countries)
          
        
          
        for i in range(0, len(all_countries)-1):
            for k in range(i+1, len(all_countries)-1):
                combined = set(all_countries[i]) & set(all_countries[k])
                if not combined:
                    # Compare categories
                    app_a_categories = applications[i].categories.all()
                    app_b_categories = applications[k].categories.all()
                    
                    a_set1 = set()
                    b_set1 = set()
                    
                    for category in app_a_categories:                        
                        a_set1.add(category.id)
                    for category in app_b_categories:
                        b_set1.add(category.id)
                    ab_set1 = a_set1 & b_set1
                    
                    version_a = Version.objects.filter(application=applications[i])[0]
                    version_b = Version.objects.filter(application=applications[k])[0]
                    
                    bundle_a_split = version_a.bundle_id.split(".")[:-1]
                    bundle_b_split = version_b.bundle_id.split(".")[:-1]
                    
                    print version_a.bundle_id + " -> " + ''.join(bundle_a_split)
                    print version_b.bundle_id + " -> " + ''.join(bundle_b_split)
                    
                    
                    
                    if len(ab_set1) is len(a_set1) and ''.join(bundle_a_split) is ''.join(bundle_b_split): #and applications[i].title == applications[k].title:
                        prompt = "> "
                        print "Match? " + applications[i].title + " and " + applications[k].title + " are similar."
                        
                        print ""
                        print "Application comparison:"
                        print "Title: " + applications[i].title + " and " + applications[k].title
                        print "Slug: " + applications[i].slug + " and " + applications[k].slug
                        print "Icon URL: " + applications[i].img_small + " and " + applications[k].img_small
                        #print "Categories: " + list(applications[i].categories.all()) + " and " + list(applications[k].categories.all())
                        
                        print ""
                        print "Version comparison:"
                        version_a = Version.objects.filter(application=applications[i])[0]
                        version_b = Version.objects.filter(application=applications[k])[0]
                        print "Country: " + version_a.country + " and " + version_b.country
                        print "Local title: " + version_a.title + " and " + version_b.title
                        print "Appstore_id: " + str(version_a.appstore_id) + " and " + str(version_b.appstore_id)
                        print "Bundle_id: " + version_a.bundle_id + " and " + version_b.bundle_id
                        print "Price/currency: " + str(version_a.price) + " " + version_a.currency + " and " + str(version_b.price) + " " + version_b.currency
                        print "Release date: " + str(version_a.release_date) + " and " + str(version_b.release_date)
                        print "iTunes rating: " + str(version_a.itunes_rating.overall_rating) + " and " + str(version_b.itunes_rating.overall_rating)
                        print "iTunes rating count: " + str(version_a.itunes_rating.overall_count) + " and " + str(version_b.itunes_rating.overall_count)
                        
                        print "Combine? Y/N?"
                        answer = raw_input(prompt)
                        if answer is "y" or answer is "Y":
                            a_versions = Version.objects.filter(application=applications[i])
                            
                            
                            for version in a_versions:
                                version.application = applications[k]
                                version.save()
                                
                            for category in app_a_categories:
                                applications[i].categories.remove(category)
                                
                            applications[i].delete()
                            
                            break
                            
