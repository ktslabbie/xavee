from django.db import models

class Developer(models.Model):    
    name = models.CharField("Developer name", max_length = 64, help_text = "The name of the developer.")
    
    class Meta:
        ordering = ["-name"]
        
    def __unicode__(self):
        return u'%s' % self.name


class Application(models.Model):    
    name = models.CharField("App name", max_length = 64, help_text = "The name of the application.")
    developer = models.ForeignKey(Developer, related_name = "developers")
    date_added = models.DateTimeField(auto_now_add = True, editable = False)
    
    class Meta:
        ordering = ["-name"]
        
    def __unicode__(self):
        return u'%s' % self.name


class Platform(models.Model):    
    name = models.CharField("Platform name", max_length = 32, help_text = "The name of the platform.")
    
    class Meta:
        ordering = ["-name"]
    
    def __unicode__(self):
        return u'%s' % self.name


class Version(models.Model):
    app = models.ForeignKey(Application, related_name = "versions")
    platform = models.ForeignKey(Platform, related_name = "platforms")
    appstore_link = models.URLField(help_text = "The URL of the application page on the application store.")
    release_date = models.DateTimeField(blank = True, null = True, default = '', help_text = "Initial release date (optional).")
    date_added = models.DateTimeField(auto_now_add = True, editable = False)
    
    class Meta:
        verbose_name = "application version"
        
    def __unicode__(self):
        return u'%s (%s version)' % (self.app.name, self.platform.name)
