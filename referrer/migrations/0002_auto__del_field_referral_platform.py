# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Referral.platform'
        db.delete_column('referrer_referral', 'platform_id')


    def backwards(self, orm):
        # Adding field 'Referral.platform'
        db.add_column('referrer_referral', 'platform',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Platform'], related_name='referral_platforms', default='Android'),
                      keep_default=False)


    models = {
        'application.application': {
            'Meta': {'ordering': "['-name']", 'object_name': 'Application'},
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Developer']", 'related_name': "'developers'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'application.appversion': {
            'Meta': {'object_name': 'AppVersion'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Application']", 'related_name': "'versions'"}),
            'appstore_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Platform']", 'related_name': "'platforms'"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'default': "''", 'blank': 'True'})
        },
        'application.developer': {
            'Meta': {'ordering': "['-name']", 'object_name': 'Developer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'application.platform': {
            'Meta': {'ordering': "['-name']", 'object_name': 'Platform'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'referrer.referral': {
            'Meta': {'ordering': "['-referral_id']", 'object_name': 'Referral'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.AppVersion']", 'related_name': "'referral_versions'"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'referral_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referral_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'default': "''"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'times_clicked': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['referrer']