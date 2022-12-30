from django.urls import re_path

from badgeuser.api import BadgeUserToken, BadgeUserForgotPassword, BadgeUserEmailConfirm, BadgeUserDetail
from badgeuser.api_v1 import BadgeUserEmailList, BadgeUserEmailDetail

urlpatterns = [
    re_path(r'^auth-token$', BadgeUserToken.as_view(), name='v1_api_user_auth_token'),
    re_path(r'^profile$', BadgeUserDetail.as_view(), name='v1_api_user_profile'),
    re_path(r'^forgot-password$', BadgeUserForgotPassword.as_view(), name='v1_api_auth_forgot_password'),
    re_path(r'^emails$', BadgeUserEmailList.as_view(), name='v1_api_user_emails'),
    re_path(r'^emails/(?P<id>[^/]+)$', BadgeUserEmailDetail.as_view(), name='v1_api_user_email_detail'),
    re_path(r'^legacyconfirmemail/(?P<confirm_id>[^/]+)$', BadgeUserEmailConfirm.as_view(), name='legacy_user_email_confirm'),
    re_path(r'^confirmemail/(?P<confirm_id>[^/]+)$', BadgeUserEmailConfirm.as_view(), name='v1_api_user_email_confirm')
]
