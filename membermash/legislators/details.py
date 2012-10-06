import logging
from operator import itemgetter
import os
import requests
import sunlight
import sys

try:
    import json
except ImportError:
    import simplejson as json

try:
    sunlight.config.API_KEY = os.environ['SUNLIGHT_API_KEY']
    CRP_API_KEY = os.environ['CRP_API_KEY']
    NYT_API_KEY = os.environ['NYT_API_KEY']
except KeyError:
    sys.stderr.write("Had trouble with your data API keys.\n")
    sys.exit(1)

logging.getLogger(__name__)

def get_industry_contributions(crp_id, late_cycle=2012, early_cycle=2000):
    API_ENDPOINT = 'http://www.opensecrets.org/api/'
    cycle = late_cycle
    while cycle and cycle > early_cycle:
        crp_params = {
            "method": "candIndustry",
            "output": "json",
            "apikey": CRP_API_KEY,
            "cycle": str(cycle),
            "cid": crp_id,
        }
        r = requests.get(API_ENDPOINT, params=crp_params)
        
        try:
            raw_results = json.loads(r.text)
            industries = [item["@attributes"] for item in 
                raw_results["response"]["industries"]["industry"]]
            for item in industries:
                item["indivs"] = int(item["indivs"])
                item["pacs"] = int(item["pacs"])
                item["total"] = int(item["total"])
            industries.sort(key=itemgetter("total"), reverse=True)
        except (KeyError, ValueError), e:
            logging.error("Industries error for CRP ID %s" % crp_id)
            return []  # Not sure what happened here.
        
        if False:  # FIXME: This should be the no-results-found check.
            cycle -= 2  # Go to the previous election cycle
        else:
            return industries  # Also breaks us out of the loop
    
    logger.info("No industries results for CRP ID %s" % crp_id)
    return []  # If we're here, we've definitely got nothing.

def get_contributors(crp_id, late_cycle=2012, early_cycle=2000):
    API_ENDPOINT = 'http://www.opensecrets.org/api/'
    cycle = late_cycle
    while cycle and cycle > early_cycle:
        crp_params = {
            "method": "candContrib",
            "output": "json",
            "apikey": CRP_API_KEY,
            "cycle": str(cycle),
            "cid": crp_id,
        }
        r = requests.get(API_ENDPOINT, params=crp_params)
        
        try:
            raw_results = json.loads(r.text)
            industries = [item["@attributes"] for item in 
                raw_results["response"]["contributors"]["contributor"]]
            for item in industries:
                item["total"] = int(item["total"])
        except (KeyError, ValueError), e:
            logging.error("Contributors error for CRP ID %s" % crp_id)
            return []  # Not sure what happened here.
        
        if False:  # FIXME: This should be the no-results-found check.
            cycle -= 2  # Go to the previous election cycle
        else:
            return industries  # Also breaks us out of the loop
    
    logger.info("No contributors results for CRP ID %s" % crp_id)
    return []  # If we're here, we've definitely got nothing.

def get_introduced_bills(bioguide_id):
    API_ENDPOINT = ''.join([
        'http://api.nytimes.com/svc/politics/v3/us/legislative/congress',
        '/members/', bioguide_id, '/bills/introduced.json'
    ])
    nyt_params = {"api-key": NYT_API_KEY}
    r = requests.get(API_ENDPOINT, params=nyt_params)
    
    try:
        raw_results = json.loads(r.text)
        bills = []
        for bill in raw_results["results"][0]["bills"]:
            if bill["sponsor_id"] == bioguide_id:
                bills.append(bill)
        return bills
    except (KeyError, ValueError), e:
        logging.error("Bills error for BioGuide ID %s" % bioguide_id)
        return []

def get_agreement(bioguide_id_1, bioguide_id_2, chamber, congress='112'):
    # Get things in the format the NYT API expects
    if chamber.lower() == 'rep':
        chamber = 'house'
    elif chamber.lower() == 'sen':
        chamber = 'senate'
    
    API_ENDPOINT = ''.join([
        'http://api.nytimes.com/svc/politics/v3/us/legislative/congress',
        '/members/', bioguide_id_1, '/votes/', bioguide_id_2,
        '/', congress, '/', chamber, '.json'
    ])
    nyt_params = {"api-key": NYT_API_KEY}
    r = requests.get(API_ENDPOINT, params=nyt_params)
    
    try:
        raw_results = json.loads(r.text)
        result = raw_results["results"][0]
        return {
            "common_votes": int(result["common_votes"]),
            "disagree_votes": int(result["disagree_votes"]),
            "agree_percent": float(result["agree_percent"]),
            "disagree_percent": float(result["disagree_percent"]),
        }
    except (KeyError, ValueError), e:
        logging.error("Agreement error for BioGuide ID %s" % bioguide_id)
        return {}
