from django.utils import timezone
import requests
import yaml

from .models import Legislator

def update_legislators():
    # Keep track of when we started so we can mark people we don't update here
    # as no longer serving.
    time_started = timezone.now()
    
    # Load the YAML of current legislators from the unitedstates project.
    r = requests.get(''.join([
        'https://raw.github.com',
        '/unitedstates/congress-legislators',
        '/master/legislators-current.yaml'
    ]))
    new_people = yaml.load(r.text)
    
    # Make sure we have objects for each person, along with whatever name/ID
    # stuff we know about that person.
    for new_person in new_people:
        lookup_info = {"last_name": new_person["name"]["last"]}
        for field_name in [("first_name", "first"), ("middle_name", "middle")]:
            if field_name[1] in new_person["name"]:
                lookup_info[field_name[0]] = new_person["name"][field_name[1]]
        latest_term = new_person["terms"][-1]
        lookup_info["chamber"] = latest_term["type"]
        lookup_info["party"] = latest_term["party"][0]
        try:
            lookup_info["state"] = latest_term["state"]
        except KeyError:
            continue  # Probably the president
        
        person, created = Legislator.objects.get_or_create(**lookup_info)
        for field_name in [("bioguide_id", "bioguide"),
                           ("thomas_id", "thomas"),
                           ("lis_id", "lis"),
                           ("govtrack_id", "govtrack"),
                           ("opensecrets_id", "opensecrets"),
                           ("votesmart_id", "votesmart"),
                           ("icpsr_id", "icpsr")]:
            if field_name[1] in new_person["id"]:
                setattr(person, field_name[0], new_person["id"][field_name[1]])
        person.save()
    
    # If any Legislator instances exist that were last updated before we did
    # this, mark them as no longer serving.
    not_updated = Legislator.objects.filter(last_updated__lt=time_started)
    not_updated.update(is_active=False)
