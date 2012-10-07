from django.http import Http404
from django.shortcuts import redirect, render

from .models import Legislator

def index(request):
    return render(request, 'legislators/index.html')

def mash(request, bioguide_1=None, bioguide_2=None):
    # Things you can do:
    # get_industry_contributions(legislator_1.crp_id)
    # get_contributors(legislator_1.crp_id)
    # get_introduced_bills(legislator_1.bioguide_id)
    # get_agreement(legislator_1.bioguide_id, legislator_2.bioguide_id, legislator_1.chamber)
    raise Http404("mash")

def random(request):
    active_random = Legislator.objects.filter(is_active=True).order_by('?')
    legislator_1 = active_random[0]
    legislator_2 = active_random.filter(chamber=legislator_1.chamber)[0]
    bioguide_1 = legislator_1.bioguide_id
    bioguide_2 = legislator_2.bioguide_id
    return redirect('membermash-legislators-mash', bioguide_1=bioguide_1,
        bioguide_2=bioguide_2)
