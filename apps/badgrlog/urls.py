from django.urls import re_path

from .views import BadgrLogContextView

urlpatterns = [
    re_path(r'^v1$', BadgrLogContextView.as_view(), name='badgr_log_context'),
]
