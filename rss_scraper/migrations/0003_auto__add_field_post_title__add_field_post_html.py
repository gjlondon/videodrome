# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.title'
        db.add_column('rss_scraper_post', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10002, blank=True),
                      keep_default=False)

        # Adding field 'Post.html'
        db.add_column('rss_scraper_post', 'html',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2000000, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.title'
        db.delete_column('rss_scraper_post', 'title')

        # Deleting field 'Post.html'
        db.delete_column('rss_scraper_post', 'html')


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
            'html': ('django.db.models.fields.CharField', [], {'max_length': '2000000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'random': ('django.db.models.fields.CharField', [], {'default': "'random'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10002', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1200'})
        },
        'rss_scraper.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['rss_scraper']