
from django.urls import path, include
from watchlist_app.api.views import WatchListAV, WatchlistDetailsAV

urlpatterns = [
    path('', WatchListAV.as_view(), name='movies'),
    path('<int:pk>', WatchlistDetailsAV.as_view(), name='movie_details'),
]
