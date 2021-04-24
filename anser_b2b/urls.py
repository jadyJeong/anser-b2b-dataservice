from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('corporation', include('corporation.urls')),
    path('stock', include('stock.urls')),
]
