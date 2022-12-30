# encoding: utf-8


from django.urls import re_path

from externaltools.api import ExternalToolList, ExternalToolLaunch

urlpatterns = [
    re_path(r'^$', ExternalToolList.as_view(), name='v2_api_externaltools_list'),
    re_path(r'^launch/(?P<entity_id>[^/]+)/(?P<launchpoint>[^/]+)$', ExternalToolLaunch.as_view(), name='v2_api_externaltools_launch'),
]
