from django.http import Http404
from django.shortcuts import render

from .models import Legislator

def index(request):
    raise Http404("index")

def mash(request, bioguide_1=None, bioguide_2=None):
    raise Http404("mash")

def random(request):
    raise Http404("random")
