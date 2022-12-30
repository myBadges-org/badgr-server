from django.urls import re_path

from backpack.api import BackpackAssertionList, BackpackAssertionDetail, BackpackAssertionDetailImage, \
    BackpackCollectionList, BackpackCollectionDetail, ShareBackpackAssertion, ShareBackpackCollection
from backpack.api_v1 import CollectionLocalBadgeInstanceList, CollectionLocalBadgeInstanceDetail, \
    CollectionGenerateShare

urlpatterns = [

    re_path(r'^badges$', BackpackAssertionList.as_view(), name='v1_api_localbadgeinstance_list'),
    re_path(r'^badges/(?P<slug>[^/]+)$', BackpackAssertionDetail.as_view(), name='v1_api_localbadgeinstance_detail'),
    re_path(r'^badges/(?P<slug>[^/]+)/image$', BackpackAssertionDetailImage.as_view(), name='v1_api_localbadgeinstance_image'),

    re_path(r'^collections$', BackpackCollectionList.as_view(), name='v1_api_collection_list'),
    re_path(r'^collections/(?P<slug>[-\w]+)$', BackpackCollectionDetail.as_view(), name='v1_api_collection_detail'),

    # legacy v1 endpoints
    re_path(r'^collections/(?P<slug>[-\w]+)/badges$', CollectionLocalBadgeInstanceList.as_view(), name='v1_api_collection_badges'),
    re_path(r'^collections/(?P<collection_slug>[-\w]+)/badges/(?P<slug>[^/]+)$', CollectionLocalBadgeInstanceDetail.as_view(), name='v1_api_collection_localbadgeinstance_detail'),
    re_path(r'^collections/(?P<slug>[-\w]+)/share$', CollectionGenerateShare.as_view(), name='v1_api_collection_generate_share'),

    re_path(r'^share/badge/(?P<slug>[^/]+)$', ShareBackpackAssertion.as_view(), name='v1_api_analytics_share_badge'),
    re_path(r'^share/collection/(?P<slug>[^/]+)$', ShareBackpackCollection.as_view(), name='v1_api_analytics_share_collection'),
]
