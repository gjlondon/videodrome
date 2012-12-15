from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'', include('rss_scraper.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', direct_to_template, {"template": "homepage.html"}, name="home"),
    (r'^accounts/', include('allauth.urls')),
)
