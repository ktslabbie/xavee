# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Referral.platform'
        db.alter_column('referrer_referral', 'platform', self.gf('django.db.models.fields.CharField')(max_length=8))

    def backwards(self, orm):

        # Changing field 'Referral.platform'
        db.alter_column('referrer_referral', 'platform', self.gf('django.db.models.fields.CharField')(max_length=2))

    models = {
        'referrer.referral': {
            'Meta': {'ordering': "['-referral_id']", 'object_name': 'Referral'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'iphone'", 'max_length': '8'}),
            'referral_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referral_link': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['referrer']