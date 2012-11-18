import sys
import urllib
import urllib2
import os
from collections import defaultdict


import feedparser
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context, RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse

import rss_scraper.models as mod

def hello_world(request):
    print "hello world"


def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    return render_to_response(template_name,
        context_instance = RequestContext(request)
    )
    
def index(request):
    return render(request, 'home.html')


def get_feed(request):
    subs = get_subs()
    video_frames = []
    pass_frames = []
    blocks = defaultdict(set)
    i = 0
    for group in subs.items():
        if group[0] != "music blogs":
            continue
        for feed_uri in group[1]:
            if i > 20:
                    continue
            print "grabbing from %s" % feed_uri

            d = feedparser.parse(feed_uri)
            title = d.feed.title
            for ent in d.entries:
                if i > 20:
                    continue
                r = requests.get(ent.link)
                post = mod.Post(uri=ent.link, html=r.text)
                try:
                    soup = BeautifulSoup(r.text)
                    frames = soup.findAll("iframe")
                    for frame in frames:
                        src = frame["src"]
                        if "twitter" in src or "tumblr" in src or "facebook" in src or "comment" in src:
                            continue
                        blocks[title].add(str(frame))
                        print frame
                        i += 1
                except Exception as e:
                    
                    print e
    print video_frames
    
    for chunk in blocks:
        this_block = []
        this_block.append(chunk)
        for item in blocks[chunk]:
            this_block.append(item)
        pass_frames.append(this_block)
    
    context = {"frames": pass_frames, "other": [1,2,3]}
    return render(request, 'frames.html', context)

def test_frame(request):
    uri = '<iframe frameborder="0" height="43" scrollbars="no" scrolling="no" src="http://www.audiomack.com/embed2/xclusiveszone/hatin-on-a-youngin?btn=ff8a00&amp;bg=34342e&amp;bbg=ff8a00&amp;vbg=4d4b42&amp;vol=ff8a00&amp;dbg=ff8a00" width="100%"></iframe>'
    context = {"frame": uri, }
    return render_to_response(request, "frame_test.html", context)
    
def get_subs():

    
    username = 'george.j.london@gmail.com'
    password = os.getenv("MYPASS")
    user = mod.User(email=username)
    user.save()
    
    
    # Authenticate to obtain SID
    auth_url = 'https://www.google.com/accounts/ClientLogin'
    auth_req_data = urllib.urlencode({'Email': username,
                                      'Passwd': password,
                                      'service': 'reader'})
    auth_req = urllib2.Request(auth_url, data=auth_req_data)
    auth_resp = urllib2.urlopen(auth_req)
    auth_resp_content = auth_resp.read()
    auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
    auth_token = auth_resp_dict["Auth"]
    # Create a cookie in the header using the SID 
    header = {}
    header['Authorization'] = 'GoogleLogin auth=%s' % auth_token
    
    reader_base_url = 'http://www.google.com/reader/api/0/subscription/list'
    reader_url = reader_base_url 
    reader_req = urllib2.Request(reader_url, None, header)
    reader_resp = urllib2.urlopen(reader_req)
    reader_resp_content = reader_resp.read()

    root = ET.fromstring(str(reader_resp_content))
    feeds = defaultdict(set)
    for obj in root[0]:
        for line in obj:
            if line.attrib["name"] == "id":
                feed_uri = line.text.split("/",1)[1]
            if line.attrib["name"] == "categories":
                for child_obj in line:
                    for item in child_obj:
                        if item.attrib["name"] == "label":
                            label = item.text.rsplit("/",1)[-1]
        feeds[label].add(feed_uri) 
    for item in feeds:
        for feed in feeds[item]:
            this_feed = mod.Feed(feed_uri = feed, category = item)
            this_feed.save()
    return feeds        
                
        