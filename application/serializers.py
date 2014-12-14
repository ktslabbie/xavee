'''
Created on Jun 8, 2014

@author: Kristian
'''
from rest_framework import serializers
from .models import Application, IPhoneVersion, Ranking, WorldRanking, Developer, Category

class JSONField(serializers.WritableField):
    def to_native(self, obj):
        return obj

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        
class RankingSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='category')
    
    class Meta:
        model = Ranking
        fields = ('ranking_type', 'since', 'category', 'rank',)

class SimpleDeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id', 'ios_id', 'android_id', 'name', 'slug',)

class SimpleIPhoneVersionSerializer(serializers.ModelSerializer):
    rankings = RankingSerializer(many=True)
    
    class Meta:
        model = IPhoneVersion
        fields = ('id', 'country', 'title', 'appstore_id', 'bundle_id', 'price', 'currency', 'release_date', 
                  'overall_rating', 'overall_count', 'rankings', 'created_at',)

class SimpleApplicationSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(source='categories')
    
    class Meta:
        model = Application
        fields = ('id', 'title', 'slug', 'categories', 'img_small', 'xavee_score',)

class DeveloperSerializer(serializers.ModelSerializer):
    developer_applications = SimpleApplicationSerializer(many=True)
    
    class Meta:
        model = Developer
        fields = ('id', 'ios_id', 'android_id', 'name', 'slug', 'created_at', 'updated_at', 'developer_applications',)


class IPhoneVersionSerializer(serializers.ModelSerializer):
    application = SimpleApplicationSerializer(source='application')
    rankings = RankingSerializer(many=True)
    
    class Meta:
        model = IPhoneVersion
        fields = ('id', 'country', 'title', 'application', 'appstore_id', 'bundle_id', 'price', 'currency', 
                  'release_date', 'overall_rating', 'overall_count', 'rankings', 'created_at', 'updated_at',)


class ApplicationSerializer(serializers.ModelSerializer):
    developer = SimpleDeveloperSerializer(source='developer')
    categories = CategorySerializer(source='categories')
    iphone_versions = SimpleIPhoneVersionSerializer(source='iphone_versions')
    
    class Meta:
        model = Application
        fields = ('id', 'title', 'slug', 'developer', 'categories', 'img_small', 'itunes_world_rating', 
                  'itunes_world_rating_count', 'xavee_score', 'iphone_versions', 'created_at', 'updated_at',)


class WorldRankingSerializer(serializers.ModelSerializer):
    ranking = JSONField()
    
    class Meta:
        model = WorldRanking
        fields = ('country', 'ranking_type', 'since', 'platform', 'category', 'currency', 'ranking')
