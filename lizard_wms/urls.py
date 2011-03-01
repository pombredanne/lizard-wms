# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

ITEM_MODELS = ['wmssource', ]  # for maptree items.

urlpatterns = patterns(
    '',
    url(r'^$',
        'lizard_maptree.views.homepage',
        {'title': 'WMS', 'item_models': ITEM_MODELS},
        name='lizard_wms.homepage'),
    url(r'^category/(?P<root_slug>.*)/$',
        'lizard_maptree.views.homepage',
        {'title': 'WMS', 'item_models': ITEM_MODELS},
        name='lizard_wms.homepage'),
    (r'^map/', include('lizard_map.urls')),
    )


if settings.DEBUG:
    # Add this also to the projects that use this application
    urlpatterns += patterns(
        '',
        (r'^admin/', include(admin.site.urls)),
        (r'', include('staticfiles.urls')),
    )
