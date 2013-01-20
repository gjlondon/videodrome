from django.conf.urls import patterns, url
from django.shortcuts import render
from django.views.generic.simple import direct_to_template

from rss_scraper import views

urlpatterns = patterns('',
    url(r'feed', views.get_feed, name='get_feed'),
    url(r'refed', views.refresh_frames, name='refresh_frames'),
    url(r'^test/$', views.test_frame),
    
)