from django.db import models
from django.utils.text import slugify
from django.contrib.sites.models import Site
from approduce.util import build_url

# Create your models here.
class Referral(models.Model):
    referral_link = models.URLField(default = '', editable = False)
    name = models.CharField("App name", max_length = 256, help_text = "The name of the app.")
    source = models.CharField(max_length = 32, help_text = "The site that will host the referrer link (e.g. 'appbank').")
    medium = models.CharField(max_length = 32, help_text = "The medium used (e.g. 'review').")
    destination = models.URLField(help_text = "Copy/paste the app store URL here.")
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "referral link"
        
    def save(self, *args, **kwargs):
        self.name = slugify(self.name).replace('-','_')
        self.source = slugify(self.source).replace('-','_')
        self.medium = slugify(self.medium).replace('-','_')
        
        path = build_url("referrer:referral", get = {'utm_source': self.source, 'utm_medium': self.medium, 'utm_campaign': self.name,})
        current_site = Site.objects.get_current()
        self.referral_link = "http://%s%s" % (current_site, path)
            
        super(Referral, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u'%s' % self.referral_link