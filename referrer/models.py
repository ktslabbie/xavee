from django.db import models
from django.conf import settings
from django.utils.text import slugify
    
class Referral(models.Model):
    referral_id = models.AutoField(primary_key = True)
    referral_link = models.URLField(default = '', editable = False)
    
    IPHONE = 'iphone'
    ANDROID = 'android'
    WINDOWS = 'windows'
    KINDLE = 'kindle'
    
    PLATFORM_CHOICES = (
        (IPHONE, 'iPhone'),
        (ANDROID, 'Android'),
        (WINDOWS, 'Windows Phone'),
        (KINDLE, 'Kindle'),
    )
    
    platform = models.CharField(max_length = 8, choices = PLATFORM_CHOICES, default = IPHONE)
    name = models.CharField("App name", max_length = 64, help_text = "The name of the app.")
    source = models.CharField(max_length = 16, help_text = "The name of the site that will host the referrer link (e.g. 'appbank').")
    medium = models.CharField(max_length = 16, help_text = "The medium used (e.g. 'review').")
    destination = models.URLField(help_text = "Copy/paste the app store URL here.")
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    
    class Meta:
        ordering = ["-referral_id"]
        verbose_name = "referral link"
        
    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        self.source = slugify(self.source)
        self.medium = slugify(self.medium)
        
        #path = build_url("referral", get = {'utm_source': self.source, 'utm_medium': self.medium, 'utm_campaign': self.name,})
        #current_site = Site.objects.get_current()
        super(Referral, self).save(*args, **kwargs)
        
        self.referral_link = settings.REFERRAL_SITE + "/%s/%s?r=%s" % (self.platform, self.name, self.referral_id)
        super(Referral, self).save(update_fields=['referral_link'])
        
    def __unicode__(self):
        return u'%s' % self.referral_link

