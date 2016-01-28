from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [
               url(r'^cluster/', include('zookeeper_dashboard.zkadmin.urls')),
               url(r'^tree/', include('zookeeper_dashboard.zktree.urls')),
               url(r'^$', include('zookeeper_dashboard.zkadmin.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
