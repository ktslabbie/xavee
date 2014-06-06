# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Application.date_added'
        db.add_column('application_application', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 6, 0, 0), blank=True, auto_now_add=True),
                      keep_default=False)

        # Adding field 'Version.date_added'
        db.add_column('application_version', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 6, 0, 0), blank=True, auto_now_add=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Application.date_added'
        db.delete_column('application_application', 'date_added')

        # Deleting field 'Version.date_added'
        db.delete_column('application_version', 'date_added')


    models = {
        'application.application': {
            'Meta': {'object_name': 'Application', 'ordering': "['-name']"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Platform']", 'related_name': "'platforms'"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['application']