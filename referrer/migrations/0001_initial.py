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
            ('clicked_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('destination', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('app_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('click_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('referrer', ['Referral'])


    def backwards(self, orm):
        # Deleting model 'Referral'
        db.delete_table('referrer_referral')


    models = {
        'referrer.referral': {
            'Meta': {'object_name': 'Referral', 'ordering': "['referral_id']"},
            'app_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'click_number': ('django.db.models.fields.IntegerField', [], {}),
            'clicked_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'referral_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['referrer']