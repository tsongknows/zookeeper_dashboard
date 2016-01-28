from django.conf.urls import url
from zookeeper_dashboard.zktree.views import index

urlpatterns = [
               url(r'^(?P<path>.*)/$', index),
               url(r'^$', index)
]
