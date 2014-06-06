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
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(related_name='referral_platforms', to=orm['application.Platform'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(related_name='referral_versions', to=orm['application.AppVersion'])),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('times_clicked', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('referrer', ['Referral'])


    def backwards(self, orm):
        # Deleting model 'Referral'
        db.delete_table('referrer_referral')


    models = {
        'application.application': {
            'Meta': {'object_name': 'Application', 'ordering': "['-name']"},
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'developers'", 'to': "orm['application.Developer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'application.appversion': {
            'Meta': {'object_name': 'AppVersion'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['application.Application']"}),
            'appstore_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'platforms'", 'to': "orm['application.Platform']"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'default': "''"})
        },
        'application.developer': {
            'Meta': {'object_name': 'Developer', 'ordering': "['-name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'application.platform': {
            'Meta': {'object_name': 'Platform', 'ordering': "['-name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'referrer.referral': {
            'Meta': {'object_name': 'Referral', 'ordering': "['-referral_id']"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'referral_versions'", 'to': "orm['application.AppVersion']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'referral_platforms'", 'to': "orm['application.Platform']"}),
            'referral_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referral_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'default': "''"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'times_clicked': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['referrer']