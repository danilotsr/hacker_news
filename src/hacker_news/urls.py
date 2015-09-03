from django.conf.urls import include, url
from django.contrib import admin

from hacker_news import views

DATE_REGEX = '[0-9-:\s]+'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(\d+)/queries/count/(%s)$' % DATE_REGEX, views.count),
    url(r'^(\d+)/queries/popular/(%s)$' % DATE_REGEX, views.popular),
    url(r'^(\d+)/build_index$', views.build_index),
]
