from django.db import models

# Create your models here.
class Referral(models.Model):
    referral_id = models.AutoField(primary_key=True)
    clicked_at = models.DateTimeField(auto_now_add = True, editable = False)
    origin = models.CharField(max_length = 255)
    destination = models.URLField()
    app_title = models.CharField(max_length = 255)
    click_number = models.IntegerField(default=0)
    
    class Meta:
        ordering = ["referral_id"]
        
    def __unicode__(self):
        return u'%s' % self.app_title
    
#    @models.permalink
#    def get_absolute_url(self):
#        return ("referrer:referral", (), {"id": self.id})