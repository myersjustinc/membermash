from django.utils import timezone

from csv import DictReader
from io import StringIO
import requests

from .models import Legislator

def update_legislators():
    # Keep track of when we started so we can mark people we don't update here
    # as no longer serving.
    time_started = timezone.now()
    
    # Load the YAML of current legislators from the unitedstates project.
    r = requests.get(''.join([
        'https://raw.github.com',
        '/sunlightlabs/apidata',
        '/master/legislators/legislators.csv'
    ]))
    input_file = StringIO()
    input_file.write(r.text)
    input_file.seek(0)
    reader = DictReader(input_file)
    
    # Make sure we have objects for each person, along with whatever name/ID
    # stuff we know about that person.
    for row in reader:
        if row["in_office"] != '1':
            continue
        
        lookup_info = {"last_name": row["lastname"]}
        for field_name in [("first_name", "firstname"),
                ("middle_name", "middlename"), ("nickname", "nickname")]:
            if field_name[1] in row:
                lookup_info[field_name[0]] = row[field_name[1]]
        lookup_info["chamber"] = row["title"].lower()
        lookup_info["party"] = row["party"]
        lookup_info["state"] = row["state"]
        
        person, created = Legislator.objects.get_or_create(**lookup_info)
        for field_name in ["bioguide_id", "votesmart_id", "fec_id",
                "govtrack_id", "crp_id", "gender", "phone", "fax", "website",
                "twitter_id", "facebook_id"]:
            setattr(person, field_name, row[field_name])
        person.save()
    
    # If any Legislator instances exist that were last updated before we did
    # this, mark them as no longer serving.
    not_updated = Legislator.objects.filter(last_updated__lt=time_started)
    not_updated.update(is_active=False)
