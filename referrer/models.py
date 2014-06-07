from django.db import models
from django.conf import settings
from django.utils.text import slugify
from application.models import Version
    
class Referral(models.Model):
    referral_id = models.AutoField(primary_key = True)
    referral_link = models.URLField(default = '', editable = False)    
    app = models.ForeignKey(Version, related_name = "referral_versions")
    source = models.CharField(max_length = 16, help_text = "The name of the site that will host the referrer link (e.g. 'appbank').")
    medium = models.CharField(max_length = 16, help_text = "The medium used (e.g. 'review, ad').")
    times_clicked = models.IntegerField("Times clicked", default = 0)
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    
    class Meta:
        ordering = ["-referral_id"]
        verbose_name = "referral link"
        
    def save(self, *args, **kwargs):
        super(Referral, self).save(*args, **kwargs)
        self.referral_link = settings.REFERRAL_HOST + "/%s/%s?r=%s" % (self.app.platform.name, slugify(self.app.app.name), self.referral_id)
        super(Referral, self).save(update_fields=['referral_link'])
    
    def update_clicks(self):
        self.times_clicked += 1
        super(Referral, self).save(update_fields=['times_clicked'])
        
    def __unicode__(self):
        return u'%s' % self.referral_link
