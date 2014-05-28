# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Referral'
        db.create_table('referrer_referral', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referral_link', self.gf('django.db.models.fields.URLField')(default='', max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('destination', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('referrer', ['Referral'])


    def backwards(self, orm):
        # Deleting model 'Referral'
        db.delete_table('referrer_referral')


    models = {
        'referrer.referral': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Referral'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'referral_link': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['referrer']