from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
import rss_scraper
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'', include('rss_scraper.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', direct_to_template, {"template": "homepage.html"}, name="home"),
    (r'^accounts/', include('allauth.urls')),
    url(r'^api/(?P<username>\w*)/post/next/$', 'rss_scraper.views.next', name="next"),
    url(r'^api/(?P<username>\w*)/post/(?P<num>\d*)$', 'rss_scraper.views.get_frame_by_id', name="next"),

)
