'''
Created on Jun 8, 2014

@author: Kristian
'''
from rest_framework import serializers
from .models import Application, Version, WorldRanking, Developer

class JSONField(serializers.WritableField):
    def to_native(self, obj):
        return obj


class DeveloperSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Developer
        fields = ('id', 'ios_id', 'android_id', 'name', 'slug', 'created_at', 'updated_at',)
        #lookup_field = 'slug'

class ApplicationSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(source='developer')
    
    class Meta:
        model = Application
        fields = ('id', 'title', 'slug', 'developer', 'categories', 'img_small', 'created_at', 'updated_at',)
        #lookup_field = 'slug'
        
class VersionSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(source='application')
    
    class Meta:
        model = Version
        fields = ('id', 'country', 'title', 'application', 'appstore_id', 'bundle_id', 'price', 'currency', 'release_date', 'created_at', 'updated_at',)
        #lookup_field = 'country'

class RankingSerializer(serializers.ModelSerializer):
    version = VersionSerializer(source='version')
    ranking = JSONField()
    
    class Meta:
        model = WorldRanking
        fields = ('country', 'ranking_type', 'since', 'platform', 'category', 'ranking')
