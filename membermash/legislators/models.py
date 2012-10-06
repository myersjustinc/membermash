from django.db import models
from django.contrib.localflavor.us.models import USStateField

CHAMBER_CHOICES = (
    ("rep", "House"),
    ("sen", "Senate"),
)
PARTY_CHOICES = (
    ("R", "Republican"),
    ("D", "Democratic"),
    ("I", "Independent"),
)

class Legislator(models.Model):
    is_active = models.BooleanField(default=True, help_text="Is this person currently serving?")
    last_updated = models.DateTimeField(auto_now=True)
    
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    
    chamber = models.CharField(max_length=3, choices=CHAMBER_CHOICES)
    party = models.CharField(max_length=1, choices=PARTY_CHOICES)
    state = USStateField()
    
    bioguide_id = models.CharField(max_length=25, blank=True)
    thomas_id = models.CharField(max_length=25, blank=True)
    lis_id = models.CharField(max_length=25, blank=True)
    govtrack_id = models.CharField(max_length=25, blank=True)
    opensecrets_id = models.CharField(max_length=25, blank=True)
    votesmart_id = models.CharField(max_length=25, blank=True)
    icpsr_id = models.CharField(max_length=25, blank=True)
    
    def __unicode__(self):
        name_components = []
        name_components.extend([self.chamber.title(), '. '])
        if self.first_name:
            name_components.extend([self.first_name, ' '])
        if self.middle_name:
            name_components.extend([self.middle_name, ' '])
        name_components.extend([self.last_name, ' ('])
        name_components.extend([self.party, '-'])
        name_components.extend([self.state, ')'])
        return u''.join(name_components)
