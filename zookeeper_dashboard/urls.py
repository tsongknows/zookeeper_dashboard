from django.conf.urls import url

urlpatterns = [
               url(r'^cluster/', include('zookeeper_dashboard.zkadmin.urls')),
               url(r'^tree/', include('zookeeper_dashboard.zktree.urls')),
               url(r'^$', include('zookeeper_dashboard.zkadmin.urls')),
]