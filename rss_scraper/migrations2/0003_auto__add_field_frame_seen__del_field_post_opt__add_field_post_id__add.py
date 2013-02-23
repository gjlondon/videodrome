# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Frame.seen'
        db.add_column('rss_scraper_frame', 'seen',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Post.opt'
        db.delete_column('rss_scraper_post', 'opt')

        # Adding field 'Post.id'
        db.add_column('rss_scraper_post', 'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Adding field 'Post.feed'
        db.add_column('rss_scraper_post', 'feed',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['rss_scraper.Feed']),
                      keep_default=False)


        # Changing field 'Post.uri'
        db.alter_column('rss_scraper_post', 'uri', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1200))

    def backwards(self, orm):
        # Deleting field 'Frame.seen'
        db.delete_column('rss_scraper_frame', 'seen')


        # User chose to not deal with backwards NULL issues for 'Post.opt'
        raise RuntimeError("Cannot reverse this migration. 'Post.opt' and its values cannot be restored.")
        # Deleting field 'Post.id'
        db.delete_column('rss_scraper_post', 'id')

        # Deleting field 'Post.feed'
        db.delete_column('rss_scraper_post', 'feed_id')


        # Changing field 'Post.uri'
        db.alter_column('rss_scraper_post', 'uri', self.gf('django.db.models.fields.CharField')(max_length=1200, primary_key=True))

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