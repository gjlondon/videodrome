# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Post.title'
        db.delete_column('rss_scraper_post', 'title')

        # Deleting field 'Post.html'
        db.delete_column('rss_scraper_post', 'html')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Post.title'
        raise RuntimeError("Cannot reverse this migration. 'Post.title' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Post.html'
        raise RuntimeError("Cannot reverse this migration. 'Post.html' and its values cannot be restored.")

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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'random': ('django.db.models.fields.CharField', [], {'default': "'random'", 'max_length': '10'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1200'})
        },
        'rss_scraper.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['rss_scraper']