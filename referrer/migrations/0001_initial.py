# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Referral'
        db.create_table('referrer_referral', (
            ('referral_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referral_link', self.gf('django.db.models.fields.URLField')(max_length=200, default='')),
            ('platform', self.gf('django.db.models.fields.CharField')(max_length=8, default='iPhone')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('destination', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('times_clicked', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('referrer', ['Referral'])


    def backwards(self, orm):
        # Deleting model 'Referral'
        db.delete_table('referrer_referral')


    models = {
        'referrer.referral': {
            'Meta': {'ordering': "['-referral_id']", 'object_name': 'Referral'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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