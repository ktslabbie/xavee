# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'IPhoneVersion', fields ['country']
        db.create_index(u'application_iphoneversion', ['country'])

        # Adding index on 'IPhoneVersion', fields ['appstore_id']
        db.create_index(u'application_iphoneversion', ['appstore_id'])


    def backwards(self, orm):
        # Removing index on 'IPhoneVersion', fields ['appstore_id']
        db.delete_index(u'application_iphoneversion', ['appstore_id'])

        # Removing index on 'IPhoneVersion', fields ['country']
        db.delete_index(u'application_iphoneversion', ['country'])


    models = {
        u'application.application': {
            'Meta': {'ordering': "['title']", 'object_name': 'Application'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories'", 'symmetrical': 'False', 'to': u"orm['application.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'developers'", 'to': u"orm['application.Developer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_small': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'itunes_world_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '3', 'decimal_places': '2'}),
            'itunes_world_rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.category': {
            'Meta': {'ordering': "['id']", 'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.developer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Developer'},
            'android_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ios_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '256', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.iphoneversion': {
            'Meta': {'object_name': 'IPhoneVersion'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iphone_versions'", 'to': u"orm['application.Application']"}),
            'appstore_id': ('django.db.models.fields.IntegerField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'bundle_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'us'", 'max_length': '2', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'current_version_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'current_version_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'overall_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.worldranking': {
            'Meta': {'object_name': 'WorldRanking'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'world_rankings'", 'null': 'True', 'to': u"orm['application.Category']"}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'us'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'ranking': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'ranking_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'since': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['application']