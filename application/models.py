"""
Created on Jul 30, 2014

Models for application.

@author: Kristian
"""
from django.db import models
from core.models import BaseModel
from core import dicts
from unidecode import unidecode
from django.template import defaultfilters
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
import itertools

class Developer(BaseModel):
    ''' Database model for developers. '''
    ios_id      = models.IntegerField("iOS ID", help_text="The artist ID from iTunes.", blank=True, null=True, unique=True)
    android_id  = models.CharField("Android ID", help_text="The developer ID from Google Play.", max_length=128, blank=True, null=True, unique=True)
    name        = models.CharField("Developer name", max_length=256)
    slug        = models.SlugField("Developer slug", max_length=256, unique=True, blank=True, default='')
    xavee_score = models.SmallIntegerField("Xavee Score", null=True)
    
    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        ''' Custom save function. '''
        
        # If the slug field hasn't been filled in...
        if not self.slug:
            # Slugify the title.
            self.slug = defaultfilters.slugify(unidecode(self.name))
        
            # Enforce max 256 character slug length.
            self.slug = (self.slug[:251] + '..') if len(self.slug) > 253 else self.slug 
        
        orig = self.slug
        
        # Make sure the slug doesn't exists yet. Add a number postfix if so.
        if not Developer.objects.filter(pk=self.id).exists():
            for x in itertools.count(1):
                if not Developer.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
            
        super(Developer, self).save(*args, **kwargs)
        
        
    def __unicode__(self):
        return u'%s' % self.name


class Category(BaseModel):
    ''' Database model for categories. '''
    id = models.IntegerField("Category ID", primary_key=True, help_text="The ID of the category (based on iTunes genre IDs).")
    name = models.CharField("Category name", max_length=64)
    
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "categories"
        
    def __unicode__(self):
        return u'%s' % self.name


class Application(BaseModel):
    ''' Database model for applications. '''
    title = models.CharField("App title", max_length=256, db_index=True, help_text="The main title of the application (English preferred).")
    slug = models.SlugField(max_length=256, unique=True, blank=True, default='')
    developer = models.ForeignKey(Developer, related_name="developer_applications")
    categories = models.ManyToManyField(Category, related_name="categories")
    img_small = models.URLField(help_text="A link to a small size image (60px from iTunes).")
    price = models.DecimalField(decimal_places=2, max_digits=8, help_text="Price in the preferred currency. 0 if free.")
    currency = models.CharField(help_text="Three-letter currency code.", max_length=3)
    release_date = models.DateTimeField(blank=True, null=True, help_text="Initial release date (optional).")
    itunes_world_rating = models.DecimalField("iTunes World Rating", decimal_places=2, max_digits=3, null=True, default=0)
    itunes_world_rating_count = models.IntegerField("iTunes World Rating Count", null=True, default=0)
    xavee_score = models.SmallIntegerField("Xavee Score", null=True, default=0)
    multi_build = models.BooleanField("Has multiple builds", default=False)
    iap_count = models.SmallIntegerField("Number of IAPs", default=0)
    iap_sum = models.DecimalField("Sum of IAPs", decimal_places=2, max_digits=10, default=0)
    review_quality = models.SmallIntegerField("Review quality", null=True, default=0)
    
    class Meta:
        ordering = ["-itunes_world_rating_count"]
        
    def save(self, *args, **kwargs):
        ''' Custom save function. '''
        
        # If the slug field hasn't been filled in...
        if not self.slug:
            # Slugify the title.
            self.slug = defaultfilters.slugify(unidecode(self.title))
        
            # Enforce max 256 character slug length.
            self.slug = (self.slug[:251] + '..') if len(self.slug) > 253 else self.slug 
        
        orig = self.slug
        if not Application.objects.filter(pk=self.id).exists():
            for x in itertools.count(1):
                if not Application.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
            
        super(Application, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u'%s' % self.title
    

class IPhoneVersion(BaseModel):
    ''' Database model for app versions (Android version, iOS version, etc.). '''
    application = models.ForeignKey(Application, related_name="iphone_versions")
    country = models.CharField(max_length=2, choices=dicts.COUNTRY_CHOICES.items(), default='us')
    title = models.CharField("App title", max_length=256, help_text="The title of the application in the local language.")
    appstore_id = models.IntegerField("Appstore ID", blank=True, null=True, default='', db_index=True, help_text="This is the ID from the iTunes app store.")
    bundle_id = models.CharField("Bundle name", max_length=256, help_text="This is the package name of the app.")
    price = models.DecimalField(decimal_places=2, max_digits=8, help_text="Price in the local currency. 0 if free.")
    currency = models.CharField(help_text="Three-letter currency code.", max_length=3)
    release_date = models.DateTimeField(blank=True, null=True, default='', help_text="Initial release date (optional).")
    current_version_rating = models.DecimalField(decimal_places=1, max_digits=2, null=True, default=0)
    current_version_count = models.PositiveIntegerField(null=True, default=0)
    overall_rating = models.DecimalField(decimal_places=1, max_digits=2, null=True, default=0)
    overall_count = models.PositiveIntegerField(null=True, default=0)
    
    class Meta:
        verbose_name = "iPhone version"
        
    def __unicode__(self):
        return u'%s (iPhone version)' % (self.application.title)


class Ranking(models.Model):
    ''' Database model for App version rankings. '''
    version = models.ForeignKey(IPhoneVersion, related_name='rankings')
    ranking_type = models.SmallIntegerField(choices=dicts.TYPE_CHOICES, default=dicts.TOP_GROSSING)
    since = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=True, related_name='rankings')
    rank = models.SmallIntegerField(null=False, default=-1)

    class Meta:
        ordering = ["rank"]
      
    def __unicode__(self):
        return u'%s' % self.rank

class WorldRanking(models.Model):
    ''' Database model for App version world rankings. '''
    ranking_type = models.SmallIntegerField(choices=dicts.TYPE_CHOICES, default=dicts.TOP_GROSSING)
    since = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=True, related_name='world_rankings')
    platform = models.SmallIntegerField(choices=dicts.PLATFORM_CHOICES, default=1)
    country = models.CharField(max_length=2, choices=dicts.COUNTRY_CHOICES.items(), default='us')
    currency = models.CharField(help_text="Three-letter currency code.", max_length=3)
    ranking = JSONField()
    
    def __unicode__(self):
        return u'%s' % self.type

    