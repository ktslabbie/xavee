# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Developer'
        db.create_table(u'application_developer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('ios_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('android_id', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=256, blank=True)),
        ))
        db.send_create_signal(u'application', ['Developer'])

        # Adding model 'Category'
        db.create_table(u'application_category', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'application', ['Category'])

        # Adding model 'Application'
        db.create_table(u'application_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=256, blank=True)),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='developers', to=orm['application.Developer'])),
            ('img_small', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('itunes_world_rating', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=3, decimal_places=2)),
            ('itunes_world_rating_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'application', ['Application'])

        # Adding M2M table for field categories on 'Application'
        m2m_table_name = db.shorten_name(u'application_application_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm[u'application.application'], null=False)),
            ('category', models.ForeignKey(orm[u'application.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['application_id', 'category_id'])

        # Adding model 'IPhoneVersion'
        db.create_table(u'application_iphoneversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='iphone_versions', to=orm['application.Application'])),
            ('country', self.gf('django.db.models.fields.CharField')(default='us', max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('appstore_id', self.gf('django.db.models.fields.IntegerField')(default='', null=True, blank=True)),
            ('bundle_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(default='', null=True, blank=True)),
            ('current_version_rating', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=2, decimal_places=1)),
            ('current_version_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('overall_rating', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=2, decimal_places=1)),
            ('overall_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'application', ['IPhoneVersion'])

        # Adding model 'WorldRanking'
        db.create_table(u'application_worldranking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ranking_type', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
            ('since', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='world_rankings', null=True, to=orm['application.Category'])),
            ('platform', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('country', self.gf('django.db.models.fields.CharField')(default='us', max_length=2)),
            ('ranking', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'application', ['WorldRanking'])


    def backwards(self, orm):
        # Deleting model 'Developer'
        db.delete_table(u'application_developer')

        # Deleting model 'Category'
        db.delete_table(u'application_category')

        # Deleting model 'Application'
        db.delete_table(u'application_application')

        # Removing M2M table for field categories on 'Application'
        db.delete_table(db.shorten_name(u'application_application_categories'))

        # Deleting model 'IPhoneVersion'
        db.delete_table(u'application_iphoneversion')

        # Deleting model 'WorldRanking'
        db.delete_table(u'application_worldranking')


    models = {
        u'application.application': {
            'Meta': {'ordering': "['title']", 'object_name': 'Application'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories'", 'symmetrical': 'False', 'to': u"orm['application.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'developers'", 'to': u"orm['application.Developer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_small': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'itunes_world_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '3', 'decimal_places': '2'}),
            'itunes_world_rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.category': {
            'Meta': {'ordering': "['id']", 'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.developer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Developer'},
            'android_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ios_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '256', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.iphoneversion': {
            'Meta': {'object_name': 'IPhoneVersion'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iphone_versions'", 'to': u"orm['application.Application']"}),
            'appstore_id': ('django.db.models.fields.IntegerField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'bundle_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'us'", 'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'current_version_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'current_version_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'overall_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.worldranking': {
            'Meta': {'object_name': 'WorldRanking'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'world_rankings'", 'null': 'True', 'to': u"orm['application.Category']"}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'us'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'ranking': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'ranking_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'since': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['application']