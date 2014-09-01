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
from django.template import defaultfilters
from .models import Application, Ranking, Version, Developer, Category, ITunesRating, WorldRanking
from core import utils, dicts

logger = get_task_logger(__name__)

''' Constants '''
# iTunes domain.
IOS_DOMAIN = 'https://itunes.apple.com/'

# Get a list of the countries we're gathering apps from.
COUNTRIES = dicts.COUNTRY_CHOICES.keys()

# Initialize a dictionary to store country rankings by app (for generating rank-by-country at the end).
countryrank_by_app = {}

# Initialize the list of world rankings objects to insert to DB.
# This will be a list of dictionaries with country and a ranking dictionary. 
world_rankings = { k:[] for k in COUNTRIES }

@shared_task
def collect_all_ios_rankings(ranking_category_id, limit):
    collect_ios_ranking(dicts.TOP_FREE, ranking_category_id, limit)
    collect_ios_ranking(dicts.TOP_PAID, ranking_category_id, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, ranking_category_id, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7008, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7008, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7008, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7009, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7009, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7009, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7010, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7010, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7010, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7011, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7011, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7011, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7012, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7012, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7012, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7013, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7013, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7013, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7014, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7014, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7014, limit)
    
    collect_ios_ranking(dicts.TOP_FREE, 7015, limit)
    collect_ios_ranking(dicts.TOP_PAID, 7015, limit)
    collect_ios_ranking(dicts.TOP_GROSSING, 7015, limit)

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
    
    print("Collecting the top " + str(limit) + " " + type_string + " of category " + str(ranking_category_id) + " from " + IOS_DOMAIN + "...")
    
    # Iterate over the countries and collect rankings for each.
    for country in COUNTRIES:
        collect_ios_ranking_for_country(path, ranking_type, category, country)
    
    # Add the app rankings for foreign countries to each country ranking.
    add_apprank_by_country(ranking_type, category)
    
    # Re-initialize the ranking objects.
    global countryrank_by_app
    countryrank_by_app = {}
    global world_rankings
    world_rankings = { k:[] for k in COUNTRIES }
    
    print("All apps collected and ranked.")


def collect_ios_ranking_for_country(path, ranking_type, category, country):
    ''' Sub-function to collect a type of ranking for one country. '''
    
    # First call the appropriate RSS feed (list of top 200 apps).
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
        
        print("Currently processing " + str(rank_counter) + "th ranked app '" + app['im:name']['label'] + "' in country '" + country + "'...")
        
        # Check if we already have this Version of this app for this country in the DB.
        if not Version.objects.filter(appstore_id=appstore_id, country=country).exists():
            
            # The Version with this ID does not yet exist for this country. Let's create one.
            # We're also creating a whole new Application unless there already exists a version for another country,
            # since we're assuming one ID per application at this point.
            application = None
            version = Version.objects.filter(appstore_id=appstore_id).first()
            if version is not None:
                application = version.application
            
            # It'll be easier to just add the versions for all countries for this app in one swoop.
            for version_country in COUNTRIES:
                
                # The application should get added for the first country for which we find a version.
                # For subsequent countries the application returned is just the application passed as argument. 
                application = lookup_and_add_ios_app(appstore_id, version_country, application)
                
            # endfor: We've added versions for all countries we didn't have yet.
            
        # endif: Don't forget to get the original version of the original country we were supposed to rank. 
        version = Version.objects.get(appstore_id=appstore_id, country=country)
        
        # We should have a version now.
        assert(version is not None)
        
        # Time to create the new ranking for this version and add it to the list (we save to DB in bulk later).
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
    Ranking.objects.filter(ranking_type=ranking_type, version__country=country).delete()
    Ranking.objects.bulk_create(rankings)

def lookup_and_add_ios_app(appstore_id, version_country, application):
    '''
    This function queries app details for the current country using the lookup API, 
    and creates an application/version where none exist yet. 
    '''
    
    # First, check if this version already exists in DB. Return if it does.
    if Version.objects.filter(appstore_id=appstore_id, country=version_country).exists():
        return application
    
    print("Calling lookup API...")
    lookup_url = IOS_DOMAIN + 'lookup?id=' + str(appstore_id) + '&country=' + version_country
    
    for retry in utils.retryloop(40, timeout=120, delay=1, backoff=2):
        try:
            lookup_resp = requests.get(lookup_url)
            detail_data = json.loads(lookup_resp.text)
        except Exception:
            print("Connection failed. Retrying...")
            retry()
    
    # Check if we found something. No results means this app isn't being sold in this country.
    if detail_data['resultCount'] == 0:
        print("No result found for lookup of " + str(appstore_id) + " with country " + version_country + ".")
    
    else:
        # Found an app. Get the details. There will always be only one result.
        print("Found an app for lookup URL " + lookup_url + "!...")
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
        current_version = Version(country=version_country, title=title, application=application, platform=dicts.IPHONE, appstore_id=appstore_id,
                          bundle_id=bundle_id, price=price, currency=currency, release_date=release_date)
        current_version.save()
        
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
        rating = ITunesRating(version=current_version, current_version_rating=current_version_rating, current_version_count=current_version_count,
                              overall_rating=overall_rating, overall_count=overall_count)
        rating.save()
        
    return application

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


# def compare_app_versions():
#     
#     developers = Developer.objects.all()
#     
#     for developer in developers:
#         
#         applications = Application.objects.filter(developer=developer)
#         
#         
#         for index, application in enumerate(applications):    
#             if application.categories == applications[index+1].categories:
                
            
             
            
            
            

