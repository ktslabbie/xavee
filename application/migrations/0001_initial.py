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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
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

        # Adding model 'Version'
        db.create_table(u'application_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['application.Application'])),
            ('platform', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('country', self.gf('django.db.models.fields.CharField')(default='us', max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('appstore_id', self.gf('django.db.models.fields.IntegerField')(default='', null=True, blank=True)),
            ('bundle_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'application', ['Version'])

        # Adding model 'Ranking'
        db.create_table(u'application_ranking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rankings', to=orm['application.Version'])),
            ('ranking_type', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
            ('since', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rankings', null=True, to=orm['application.Category'])),
            ('rank', self.gf('django.db.models.fields.SmallIntegerField')(default=-1)),
        ))
        db.send_create_signal(u'application', ['Ranking'])

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

        # Adding model 'ITunesRating'
        db.create_table(u'application_itunesrating', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('version', self.gf('django.db.models.fields.related.OneToOneField')(related_name='itunes_rating', unique=True, primary_key=True, to=orm['application.Version'])),
            ('current_version_rating', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=2, decimal_places=1)),
            ('current_version_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('overall_rating', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=2, decimal_places=1)),
            ('overall_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'application', ['ITunesRating'])


    def backwards(self, orm):
        # Deleting model 'Developer'
        db.delete_table(u'application_developer')

        # Deleting model 'Category'
        db.delete_table(u'application_category')

        # Deleting model 'Application'
        db.delete_table(u'application_application')

        # Removing M2M table for field categories on 'Application'
        db.delete_table(db.shorten_name(u'application_application_categories'))

        # Deleting model 'Version'
        db.delete_table(u'application_version')

        # Deleting model 'Ranking'
        db.delete_table(u'application_ranking')

        # Deleting model 'WorldRanking'
        db.delete_table(u'application_worldranking')

        # Deleting model 'ITunesRating'
        db.delete_table(u'application_itunesrating')


    models = {
        u'application.application': {
            'Meta': {'ordering': "['title']", 'object_name': 'Application'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories'", 'symmetrical': 'False', 'to': u"orm['application.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'developers'", 'to': u"orm['application.Developer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_small': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '256', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'application.itunesrating': {
            'Meta': {'ordering': "['overall_rating']", 'object_name': 'ITunesRating'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_version_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'current_version_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'overall_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'overall_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'itunes_rating'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['application.Version']"})
        },
        u'application.ranking': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Ranking'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rankings'", 'null': 'True', 'to': u"orm['application.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {'default': '-1'}),
            'ranking_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'since': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rankings'", 'to': u"orm['application.Version']"})
        },
        u'application.version': {
            'Meta': {'object_name': 'Version'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': u"orm['application.Application']"}),
            'appstore_id': ('django.db.models.fields.IntegerField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'bundle_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'us'", 'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
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