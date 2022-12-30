from django.urls import re_path

from issuer.api import (IssuerList, IssuerDetail, IssuerBadgeClassList, BadgeClassDetail, BadgeInstanceList,
                        BadgeInstanceDetail, IssuerBadgeInstanceList, AllBadgeClassesList, BatchAssertionsIssue)
from issuer.api_v1 import FindBadgeClassDetail, IssuerStaffList

urlpatterns = [
    # re_path(r'^$', RedirectView.as_view(url='/v1/issuer/issuers', permanent=False)),

    re_path(r'^all-badges$', AllBadgeClassesList.as_view(), name='v1_api_issuer_all_badges_list'),
    re_path(r'^all-badges/find$', FindBadgeClassDetail.as_view(), name='v1_api_find_badgeclass_by_identifier'),

    re_path(r'^issuers$', IssuerList.as_view(), name='v1_api_issuer_list'),
    re_path(r'^issuers/(?P<slug>[^/]+)$', IssuerDetail.as_view(), name='v1_api_issuer_detail'),
    re_path(r'^issuers/(?P<slug>[^/]+)/staff$', IssuerStaffList.as_view(), name='v1_api_issuer_staff'),

    re_path(r'^issuers/(?P<slug>[^/]+)/badges$', IssuerBadgeClassList.as_view(), name='v1_api_badgeclass_list'),
    re_path(r'^issuers/(?P<issuerSlug>[^/]+)/badges/(?P<slug>[^/]+)$', BadgeClassDetail.as_view(), name='v1_api_badgeclass_detail'),

    re_path(r'^issuers/(?P<issuerSlug>[^/]+)/badges/(?P<slug>[^/]+)/batchAssertions$', BatchAssertionsIssue.as_view(), name='v1_api_badgeclass_batchissue'),

    re_path(r'^issuers/(?P<issuerSlug>[^/]+)/badges/(?P<slug>[^/]+)/assertions$', BadgeInstanceList.as_view(), name='v1_api_badgeinstance_list'),
    re_path(r'^issuers/(?P<slug>[^/]+)/assertions$', IssuerBadgeInstanceList.as_view(), name='v1_api_issuer_instance_list'),
    re_path(r'^issuers/(?P<issuerSlug>[^/]+)/badges/(?P<badgeSlug>[^/]+)/assertions/(?P<slug>[^/]+)$', BadgeInstanceDetail.as_view(), name='v1_api_badgeinstance_detail'),
]
