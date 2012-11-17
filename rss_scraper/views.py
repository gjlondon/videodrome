import sys

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context, RequestContext
from django.core.urlresolvers import reverse

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
    return HttpResponse("Hello, world. You're at the poll index.")