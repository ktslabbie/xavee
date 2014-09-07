from django.db import models
from django.conf import settings
from django.utils.text import slugify
    
class Referral(models.Model):
    referral_id = models.AutoField(primary_key=True)
    referral_name = models.CharField(max_length=128, default='', blank=True, help_text="Text to put in the referral link itself (e.g. 'Smart Alarm' for http://www.app-install.info/smart-alarm).")
    referral_link = models.URLField(default='', editable=True)
    # app = models.ForeignKey(IPhoneVersion, blank=True, null=True, related_name = "referral_iphone_versions")
    source = models.CharField(max_length=32, help_text="The name of the site that will host the referrer link (e.g. 'appbank').")
    medium = models.CharField(max_length=32, help_text="The medium used (e.g. 'review, ad').")
    times_clicked = models.IntegerField("Times clicked", default=0)
    destination = models.URLField(default='', editable=True, help_text="The destination URL this referral is pointing to (e.g. https://play.google.com/store/apps/details?id=com.everimaging.photoeffectstudio&hl=ja).")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        ordering = ["-referral_id"]
        verbose_name = "referral link"
        
    def save(self, *args, **kwargs):
        super(Referral, self).save(*args, **kwargs)
        self.referral_link = settings.REFERRAL_HOST + "/%s?r=%s" % (slugify(self.referral_name), self.referral_id)
        super(Referral, self).save(update_fields=['referral_link'])
    
    def update_clicks(self):
        self.times_clicked += 1
        super(Referral, self).save(update_fields=['times_clicked'])
        
    def __unicode__(self):
        return u'%s' % self.referral_link
