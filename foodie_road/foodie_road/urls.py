from django.urls import path, include

urlpatterns = [
    path('users',include('users.urls')),
    path('stores', include('stores.urls')),
    path('orders', include('orders.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)