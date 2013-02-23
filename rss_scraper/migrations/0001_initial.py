# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('rss_scraper_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('rss_scraper', ['User'])

        # Adding model 'Feed'
        db.create_table('rss_scraper_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_uri', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('rss_scraper', ['Feed'])

        # Adding M2M table for field users on 'Feed'
        db.create_table('rss_scraper_feed_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm['rss_scraper.feed'], null=False)),
            ('user', models.ForeignKey(orm['rss_scraper.user'], null=False))
        ))
        db.create_unique('rss_scraper_feed_users', ['feed_id', 'user_id'])

        # Adding model 'Post'
        db.create_table('rss_scraper_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1200)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss_scraper.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=10002)),
            ('html', self.gf('django.db.models.fields.CharField')(max_length=2000000)),
            ('random', self.gf('django.db.models.fields.CharField')(default='random', max_length=10)),
        ))
        db.send_create_signal('rss_scraper', ['Post'])

        # Adding model 'Frame'
        db.create_table('rss_scraper_frame', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss_scraper.Post'])),
            ('seen', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('rss_scraper', ['Frame'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('rss_scraper_user')

        # Deleting model 'Feed'
        db.delete_table('rss_scraper_feed')

        # Removing M2M table for field users on 'Feed'
        db.delete_table('rss_scraper_feed_users')

        # Deleting model 'Post'
        db.delete_table('rss_scraper_post')

        # Deleting model 'Frame'
        db.delete_table('rss_scraper_frame')


    models = {
        'rss_scraper.feed': {
            'Meta': {'object_name': 'Feed'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'feed_uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rss_scraper.User']", 'symmetrical': 'False'})
        },
        'rss_scraper.frame': {
            'Meta': {'object_name': 'Frame'},
            'html': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss_scraper.Post']"}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'rss_scraper.post': {
            'Meta': {'object_name': 'Post'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss_scraper.Feed']"}),
            'html': ('django.db.models.fields.CharField', [], {'max_length': '2000000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'random': ('django.db.models.fields.CharField', [], {'default': "'random'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10002'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1200'})
        },
        'rss_scraper.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['rss_scraper']