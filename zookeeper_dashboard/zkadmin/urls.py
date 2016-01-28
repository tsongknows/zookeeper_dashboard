from django.conf.urls import url
from zookeeper_dashboard.zkadmin.view import detail, index

urlpatterns = [
               url(r'^server/(?P<server_id>\d+)/$', detail),
               url(r'^$', index)
]

