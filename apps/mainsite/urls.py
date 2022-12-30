from django.apps import apps
from django.conf import settings
from django.conf.urls import include
from django.urls import re_path, path

from mainsite.admin import badgr_admin
from backpack.badge_connect_api import BadgeConnectManifestView, BadgeConnectManifestRedirectView
from mainsite.oauth2_api import AuthorizationApiView, TokenView, AuthCodeExchange, RegisterApiView

badgr_admin.autodiscover()
# make sure that any view/model/form imports occur AFTER admin.autodiscover

def django2_include(three_tuple_urlconf):
    (urls, app_name, namespace) = three_tuple_urlconf
    return include((urls, app_name), namespace=namespace)

from django.views.generic.base import RedirectView, TemplateView
from oauth2_provider.urls import base_urlpatterns as oauth2_provider_base_urlpatterns

from mainsite.views import (SitewideActionFormView, RedirectToUiLogin, DocsAuthorizeRedirect,
                            LegacyLoginAndObtainAuthToken,)
from mainsite.views import info_view, email_unsubscribe, AppleAppSiteAssociation, error404, error500

from mainsite.views import upload
from django.conf.urls.static import static

urlpatterns = [
    # Backup URLs in case the server isn't serving these directly
    re_path(r'^favicon\.png[/]?$', RedirectView.as_view(url='%simages/favicon.png' % settings.STATIC_URL, permanent=True)),
    re_path(r'^favicon\.ico[/]?$', RedirectView.as_view(url='%simages/favicon.png' % settings.STATIC_URL, permanent=True)),
    re_path(r'^robots\.txt$', RedirectView.as_view(url='%srobots.txt' % settings.STATIC_URL, permanent=True)),

    # legacy logo url redirect
    re_path(r'^static/images/header-logo-120.png$', RedirectView.as_view(url='{}images/logo.png'.format(settings.STATIC_URL), permanent=True)),

    # Apple app universal URL endpoint
    re_path(r'^apple-app-site-association', AppleAppSiteAssociation.as_view(), name="apple-app-site-association"),

    # OAuth2 provider URLs
    re_path(r'^o/authorize/?$', AuthorizationApiView.as_view(), name='oauth2_api_authorize'),
    re_path(r'^o/token/?$', TokenView.as_view(), name='oauth2_provider_token'),
    re_path(r'^o/code/?$', AuthCodeExchange.as_view(), name='oauth2_code_exchange'),
    re_path(r'^o/register/?$', RegisterApiView.as_view(), kwargs={'version': 'rfc7591'}, name='oauth2_api_register'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Badge Connect URLs
    re_path(r'^bcv1/manifest/(?P<domain>[^/]+)$', BadgeConnectManifestView.as_view(), name='badge_connect_manifest'),
    re_path(r'^\.well-known/badgeconnect.json$', BadgeConnectManifestRedirectView.as_view(), name='default_bc_manifest_redirect'),
    re_path(r'^bcv1/', include('backpack.badge_connect_urls'), kwargs={'version': 'bcv1'}),

    # Home
    re_path(r'^$', info_view, name='index'),
    re_path(r'^accounts/login/$', RedirectToUiLogin.as_view(), name='legacy_login_redirect'),

    # Admin URLs
    re_path(r'^staff/sidewide-actions$', SitewideActionFormView.as_view(), name='badgr_admin_sitewide_actions'),
    re_path(r'^staff/', django2_include(badgr_admin.urls)),

    # Service health endpoint
    re_path(r'^health', include('health.urls')),

    # Swagger Docs
    #
    # api docs
    #
    re_path(r'^docs/oauth2/authorize$', DocsAuthorizeRedirect.as_view(), name='docs_authorize_redirect'),
    re_path(r'^docs/?$', RedirectView.as_view(url='/docs/v2/', permanent=True)),  # default redirect to /v2/
    # re_path(r'^docs/', include('apispec_drf.urls')),

    # JSON-LD Context
    re_path(r'^json-ld/', include('badgrlog.urls')),

    # unversioned public endpoints
    re_path(r'^unsubscribe/(?P<email_encoded>[^/]+)/(?P<expiration>[^/]+)/(?P<signature>[^/]+)', email_unsubscribe, name='unsubscribe'),

    re_path(r'^public/', include('issuer.public_api_urls'), kwargs={'version': 'v2'}),

    # legacy share redirects
    re_path(r'', include('backpack.share_urls')),

    # Legacy Auth Token Endpoint: Deprecated and logged
    re_path(r'^api-auth/token$', LegacyLoginAndObtainAuthToken.as_view()),

    # Social Auth (oAuth2 and SAML)
    re_path(r'^account/', include('badgrsocialauth.urls')),

    # v1 API endpoints
    re_path(r'^v1/user/', include('badgeuser.v1_api_urls'), kwargs={'version': 'v1'}),
    re_path(r'^v1/user/', include('badgrsocialauth.v1_api_urls'), kwargs={'version': 'v1'}),

    re_path(r'^v1/issuer/', include('issuer.v1_api_urls'), kwargs={'version': 'v1'}),
    re_path(r'^v1/earner/', include('backpack.v1_api_urls'), kwargs={'version': 'v1'}),


    # v2 API endpoints
    re_path(r'^v2/', include('issuer.v2_api_urls'), kwargs={'version': 'v2'}),
    re_path(r'^v2/', include('badgeuser.v2_api_urls'), kwargs={'version': 'v2'}),
    re_path(r'^v2/', include('badgrsocialauth.v2_api_urls'), kwargs={'version': 'v2'}),
    re_path(r'^v2/backpack/', include('backpack.v2_api_urls'), kwargs={'version': 'v2'}),


    # External Tools
    re_path(r'^v1/externaltools/', include('externaltools.v1_api_urls'), kwargs={'version': 'v1'}),
    re_path(r'^v2/externaltools/', include('externaltools.v2_api_urls'), kwargs={'version': 'v2'}),

    re_path(r'^upload', upload, name="image_upload"),
]
# add to serve files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Test URLs to allow you to see these pages while DEBUG is True
if getattr(settings, 'DEBUG_ERRORS', False):
    urlpatterns = [
        re_path(r'^error/404/$', error404, name='404'),
        re_path(r'^error/500/$', error500, name='500'),
    ] + urlpatterns

# If DEBUG_MEDIA is set, have django serve anything in MEDIA_ROOT at MEDIA_URL
if getattr(settings, 'DEBUG_MEDIA', True):
    from django.views.static import serve as static_serve
    media_url = getattr(settings, 'MEDIA_URL', '/media/').lstrip('/')
    urlpatterns = [
        re_path(r'^media/(?P<path>.*)$', static_serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ] + urlpatterns

# If DEBUG_STATIC is set, have django serve up static files even if DEBUG=False
if getattr(settings, 'DEBUG_STATIC', True):
    from django.contrib.staticfiles.views import serve as staticfiles_serve
    static_url = getattr(settings, 'STATIC_URL', '/static/')
    static_url = static_url.replace(getattr(settings, 'HTTP_ORIGIN', 'http://localhost:8000'), '')
    static_url = static_url.lstrip('/')
    urlpatterns = [
        re_path(r'^%s(?P<path>.*)' % (static_url,), staticfiles_serve, kwargs={
            'insecure': True,
        })
    ] + urlpatterns

# Serve pattern library view only in debug mode or if explicitly declared
if getattr(settings, 'DEBUG', True) or getattr(settings, 'SERVE_PATTERN_LIBRARY', False):
    urlpatterns = [
       re_path(r'^component-library$', TemplateView.as_view(template_name='component-library.html'), name='component-library')
    ] + urlpatterns

# serve django debug toolbar if present
if settings.DEBUG and apps.is_installed('debug_toolbar'):
    try:
        import debug_toolbar
        urlpatterns = urlpatterns + [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass

handler404 = error404
handler500 = error500
