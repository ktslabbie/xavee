from django.db import models

class BaseModel(models.Model):
    """ Abstract base model to add created_at/updated_at to all models as per API best practices, in a DRY way. """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    class Meta:
        abstract = True