import sys
import urllib
import urllib2
import os
from collections import defaultdict
from random import shuffle

import feedparser
import requests
from bs4 import BeautifulSoup
import HTMLParser
import xml.etree.ElementTree as ET
from psycopg2 import IntegrityError


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context, RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import simplejson

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

def get_posts_from_feed(feed_uri):
    posts = []
    
    print "grabbing from %s" % feed_uri

    this_feed = mod.Feed.objects.get(feed_uri = feed_uri)
    d = feedparser.parse(feed_uri)
    try:
        title = d.feed.title
    except AttributeError:
        title = "Untitled"
    for ent in d.entries:
        post = None         
        ent_link = ent.link
        try:
            post = mod.Post.objects.get(uri=ent_link)
            text = post.html
        except mod.Post.DoesNotExist:
            import pdb
            #pdb.set_trace()
            post = parse_post(ent_link)
        if post:
            posts.append(post)
    return title, posts

def parse_post(link):
    found_frames = set()
    try:
        try:
            r = requests.get(link)
        except requests.ConnectionError as e:
            print "Could not connect"
            print e
            return
        text = r.text
        print "no post exists fro %s" % link
        if link and len(r.text) > 0:
            print "Link: %s" % link
            post = mod.Post(uri=link, html=text)
            post.save()
        else: 
            print "Couldn't find a post for %s" % ent
            return
        soup = BeautifulSoup(text)
        post_titles = soup.findAll("title")
        if post_titles:
            post.title = post_titles[0]
            print post.title
        else:
            print "post has no title"
        frames = soup.findAll("iframe")
        for frame in frames:
            src = frame["src"].lower()
            if "twitter" in src or "tumblr" in src or "facebook" in src or "comment" in src:
                continue
            found_frames.add(str(frame))
            frame_obj = mod.Frame.objects.filter(html=str(frame))
            if not frame:
                frame_obj = mod.Frame(html=str(frame), post = post)
                frame_obj.save()            
            print frame
    except HTMLParser.HTMLParseError as e:
        print "Soup problem", e
        return
    return found_frames
        

def get_feed(request):
    subs = get_subs()
    video_frames = []
    pass_frames = []
    blocks = defaultdict(set)
    posts_by_feed = {}
    i = 0
    # go through the subscribed feeds and grab iframes
    for group in subs.items():
        if group[0] != "music blogs":
            continue
        lis = list(group[1])
        # avoid displaying in the same order ever refresh
        if lis:
            shuffle(lis)
        else:
            continue
        for feed_uri in lis:
            if i > 20: # only get the first twenty, otherwise it takes forever
                continue
            title, posts = get_posts_from_feed(feed_uri)
            posts_by_feed[feed_uri] = posts
            i += len(posts)
            for post in posts:
                frames = mod.Frame.objects.filter(post=post)
                for frame in frames:
                    blocks[str(title)].add(frame.html)
            
    print blocks
    
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
    print "testing"
    return render(request, "frame_test.html", context)

def next(request, username):
    username = "george.j.london@gmail.com"
    found_frames = set()
    users = mod.User.objects.filter(email=username)
    if users:
        user = users[0]
    else:
        user = None 
    subs = get_subs()
    
    feeds = mod.Feed.objects.filter(users=user)
    feed_uris = set()
    for feed in feeds:
        if feed.category != "music blogs":
            continue
        else:
            feed_uri = feed.feed_uri
            feed_uris.add(feed_uri)
            print feed_uri
        
    feed_title, posts = get_posts_from_feed(feed_uri)
    print "posts: ", posts
    for post in posts:
        print post.title
        frames = parse_post(post.uri)
        for frame in frames:
            print frame
            found_frames.add(frame)
        
    uri = list(found_frames)[0]
   
    context = {"frame": uri, }
    
    from django.utils import simplejson

    some_data = {
       'title': 'Title!',
       "blog": "This Blog",
       'iframe': uri,
    }
    
    data = simplejson.dumps(some_data)
    print "testing"
    return HttpResponse(data, mimetype='application/json')

def get_frame_by_id(request, username, num):
    frame = mod.Frame.objects.exclude(html__isnull=True).exclude(html__exact="[]")
    if frame:
        html = frame.html
    else:
        html = '<iframe frameborder="0" height="43" scrollbars="no" scrolling="no" src="http://www.audiomack.com/embed2/xclusiveszone/hatin-on-a-youngin?btn=ff8a00&amp;bg=34342e&amp;bbg=ff8a00&amp;vbg=4d4b42&amp;vol=ff8a00&amp;dbg=ff8a00" width="100%"></iframe>'
    print html
    some_data = {
       'title': 'Title!',
       "blog": "This Blog",
       'iframe': html,
    }
    
    data = simplejson.dumps(some_data)
    print "id"
    return HttpResponse(data, mimetype='application/json')

def home(request):

    return render(request, "homepage.html")
    
def get_subs():

    
    username = 'george.j.london@gmail.com'
    password = os.getenv("MYPASS")
    user = mod.User.objects.filter(email=username)[0]
    if not user:
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
    # TODO rogueleaderr get post title
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
            this_feed = mod.Feed.objects.filter(feed_uri = feed)
            #print "feed %s already exists" % this_feed[0].user.all()
            if not this_feed:
                this_feed = mod.Feed(feed_uri = feed, category = item)
                this_feed.save()
                user.save()
                this_feed.users.add(user)
                print "added feed %s" % this_feed
    
    return feeds        
                
        