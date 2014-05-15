from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rack.views import UpdateSubscriptionsView
from rack.api import router


urlpatterns = [
    url(r'^$', 'coomix.views.home', name='home'),
    url(r'^manage/$', UpdateSubscriptionsView.as_view(), name='manage'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
