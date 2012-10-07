from django.conf.urls import patterns, include, url

urlpatterns = patterns('membermash.legislators.views',
    url(r'^$', 'index', name="membermash-legislators-home"),
    url(r'^mash/(?P<bioguide_1>\w+)/(?P<bioguide_2>\w+)/$', 'mash', 
        name="membermash-legislators-mash"),
    url(r'^mash/(?P<bioguide_1>\w+)/$', 'random'),
    url(r'^mash/$', 'mash_form', name="membermash-legislators-mash_form"),
    url(r'^random/$', 'random', name="membermash-legislators-random"),
)
