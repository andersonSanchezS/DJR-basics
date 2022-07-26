
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('watchlist_app.api.urls')),
    path('auth/', include('user_app.api.urls')),
]
