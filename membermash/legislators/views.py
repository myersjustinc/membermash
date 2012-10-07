from django.http import Http404
from django.shortcuts import redirect, render

import logging

from .models import Legislator
from .details import (get_agreement, get_bill, get_contributors, 
    get_industry_contributions, get_introduced_bills)

logging.getLogger(__name__)

def index(request):
    return render(request, 'legislators/index.html')

def mash(request, bioguide_1=None, bioguide_2=None, items_n=3):
    active_legislators = Legislator.objects.filter(is_active=True)
    
    try:
        legislator_1 = active_legislators.get(bioguide_id=bioguide_1)
        legislator_2 = active_legislators.get(bioguide_id=bioguide_2)
    except (Legislator.MultipleObjectsReturned, Legislator.DoesNotExist):
        logging.error("Had problems matching up %s and %s" % (
            bioguide_1, bioguide_2))
        raise Http404
    
    industries = [
        get_industry_contributions(legislator_1.crp_id)[:items_n],
        get_industry_contributions(legislator_2.crp_id)[:items_n],
    ]
    contributors = [
        get_contributors(legislator_1.crp_id)[:items_n],
        get_contributors(legislator_2.crp_id)[:items_n],
    ]
    bills = [
        get_introduced_bills(legislator_1.bioguide_id)[:items_n],
        get_introduced_bills(legislator_2.bioguide_id)[:items_n],
    ]
    agreement = get_agreement(legislator_1.bioguide_id,
        legislator_2.bioguide_id, legislator_1.chamber)
    
    context = {
        "agreement": agreement,
        "bills": bills,
        "contributors": contributors,
        "industries": industries,
        "legislators": [legislator_1, legislator_2],
    }
    
    return render(request, 'legislators/mash.html', context)

def mash_form(request):
    if "legislator_1" not in request.GET and "legislator_2" not in request.GET:
        return redirect('membermash-legislators-random')
    
    active_legislators = Legislator.objects.filter(is_active=True)
    active_random = active_legislators.order_by('?')
    try:
        if ("legislator_1" in request.GET and 
                request.GET['legislator_1'] != "RANDOM"):
            legislator_1 = active_legislators.get(
                bioguide_id=request.GET['legislator_1'])
        else:
            legislator_1 = None
        
        if ("legislator_2" in request.GET and 
                request.GET['legislator_2'] != "RANDOM"):
            legislator_2 = active_legislators.get(
                bioguide_id=request.GET['legislator_2'])
        else:
            legislator_2 = None
        
        if legislator_1 is None and legislator_2 is not None:
            legislator_1 = active_random.filter(chamber=legislator_2.chamber)[0]
        elif legislator_1 is not None and legislator_2 is None:
            legislator_2 = active_random.filter(chamber=legislator_1.chamber)[0]
        elif legislator_1 is None and legislator_2 is None:
            legislator_1 = active_random[0]
            legislator_2 = active_random.filter(chamber=legislator_1.chamber)[0]
    except (Legislator.MultipleObjectsReturned, Legislator.DoesNotExist):
        logging.error("Had problems matching up %s and %s" % (
            request.GET['legislator_1'], request.GET['legislator_2']))
        raise Http404
    
    bioguide_1 = legislator_1.bioguide_id
    bioguide_2 = legislator_2.bioguide_id
    return redirect('membermash-legislators-mash', bioguide_1=bioguide_1,
        bioguide_2=bioguide_2)

def random(request, bioguide_1=None):
    active_random = Legislator.objects.filter(is_active=True).order_by('?')
    if bioguide_1 is not None:
        legislator_1 = Legislator.objects.filter(is_active=True).get(
            bioguide_id=bioguide_1)
    else:
        legislator_1 = active_random[0]
    legislator_2 = active_random.filter(chamber=legislator_1.chamber)[0]
    bioguide_1 = legislator_1.bioguide_id
    bioguide_2 = legislator_2.bioguide_id
    return redirect('membermash-legislators-mash', bioguide_1=bioguide_1,
        bioguide_2=bioguide_2)
