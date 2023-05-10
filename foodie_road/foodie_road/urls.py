from django.urls import path, include
from django.conf.urls.static import static

from foodie_road import settings

urlpatterns = [
    path('users',include('users.urls')),
    path('stores', include ('stores.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)