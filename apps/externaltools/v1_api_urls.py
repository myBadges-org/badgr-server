# encoding: utf-8


from django.urls import re_path

from externaltools.api import ExternalToolList, ExternalToolLaunch

urlpatterns = [
    re_path(r'^$', ExternalToolList.as_view(), name='v1_api_externaltools_list'),
    re_path(r'^launch/(?P<slug>[^/]+)/(?P<launchpoint>[^/]+)$', ExternalToolLaunch.as_view(), name='v1_api_externaltools_launch'),
]