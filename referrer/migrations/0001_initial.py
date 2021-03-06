# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Referral'
        db.create_table(u'referrer_referral', (
            ('referral_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referral_name', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('referral_link', self.gf('django.db.models.fields.URLField')(default='', max_length=200)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('times_clicked', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('destination', self.gf('django.db.models.fields.URLField')(default='', max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'referrer', ['Referral'])


    def backwards(self, orm):
        # Deleting model 'Referral'
        db.delete_table(u'referrer_referral')


    models = {
        u'referrer.referral': {
            'Meta': {'ordering': "['-referral_id']", 'object_name': 'Referral'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'referral_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referral_link': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'referral_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'times_clicked': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['referrer']