# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AppVersion'
        db.delete_table('application_appversion')

        # Adding model 'Version'
        db.create_table('application_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Application'], related_name='versions')),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Platform'], related_name='platforms')),
            ('appstore_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True, default='')),
        ))
        db.send_create_signal('application', ['Version'])


    def backwards(self, orm):
        # Adding model 'AppVersion'
        db.create_table('application_appversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Platform'], related_name='platforms')),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Application'], related_name='versions')),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True, default='')),
            ('appstore_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('application', ['AppVersion'])

        # Deleting model 'Version'
        db.delete_table('application_version')


    models = {
        'application.application': {
            'Meta': {'ordering': "['-name']", 'object_name': 'Application'},
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Developer']", 'related_name': "'developers'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
        'application.version': {
            'Meta': {'object_name': 'Version'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Application']", 'related_name': "'versions'"}),
            'appstore_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Platform']", 'related_name': "'platforms'"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'default': "''"})
        }
    }

    complete_apps = ['application']