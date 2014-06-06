# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Developer'
        db.create_table('application_developer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('application', ['Developer'])

        # Adding model 'Application'
        db.create_table('application_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Developer'], related_name='developers')),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('application', ['Application'])

        # Adding model 'Platform'
        db.create_table('application_platform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('application', ['Platform'])

        # Adding model 'Version'
        db.create_table('application_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Application'], related_name='versions')),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Platform'], related_name='platforms')),
            ('appstore_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(default='', null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('application', ['Version'])


    def backwards(self, orm):
        # Deleting model 'Developer'
        db.delete_table('application_developer')

        # Deleting model 'Application'
        db.delete_table('application_application')

        # Deleting model 'Platform'
        db.delete_table('application_platform')

        # Deleting model 'Version'
        db.delete_table('application_version')


    models = {
        'application.application': {
            'Meta': {'object_name': 'Application', 'ordering': "['-name']"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Developer']", 'related_name': "'developers'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
        'application.version': {
            'Meta': {'object_name': 'Version'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Application']", 'related_name': "'versions'"}),
            'appstore_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Platform']", 'related_name': "'platforms'"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['application']