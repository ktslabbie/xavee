# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Referral.times_clicked'
        db.add_column('referrer_referral', 'times_clicked',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Referral.times_clicked'
        db.delete_column('referrer_referral', 'times_clicked')


    models = {
        'referrer.referral': {
            'Meta': {'ordering': "['-referral_id']", 'object_name': 'Referral'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '8', 'default': "'iPhone'"}),
            'referral_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referral_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'default': "''"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'times_clicked': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['referrer']