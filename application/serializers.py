'''
Created on Jun 8, 2014

@author: Kristian
'''
from rest_framework import serializers
from .models import Application, IPhoneVersion, WorldRanking, Developer, Category
from django import utils
from xavee import settings

class JSONField(serializers.WritableField):
    def to_native(self, obj):
        return obj

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)

class SimpleApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'title', 'slug', 'categories', 'img_small',)

class DeveloperSerializer(serializers.ModelSerializer):
    developers = SimpleApplicationSerializer(many=True)
    
    class Meta:
        model = Developer
        fields = ('id', 'ios_id', 'android_id', 'name', 'slug', 'created_at', 'updated_at', 'developers',)

class ApplicationSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(source='developer')
    categories = CategorySerializer(source='categories')
    
    class Meta:
        model = Application
        fields = ('id', 'title', 'slug', 'developer', 'categories', 'img_small', 'created_at', 'updated_at',)
        
class IPhoneVersionSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(source='application')
    
    class Meta:
        model = IPhoneVersion
        fields = ('id', 'country', 'title', 'application', 'appstore_id', 'bundle_id', 'price', 'currency', 'release_date', 'created_at', 'updated_at',)

class RankingSerializer(serializers.ModelSerializer):
    ranking = JSONField()
    
    class Meta:
        model = WorldRanking
        fields = ('country', 'ranking_type', 'since', 'platform', 'category', 'currency', 'ranking')
