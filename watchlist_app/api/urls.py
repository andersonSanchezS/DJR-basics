
from django.urls import path
from watchlist_app.api.views import (WatchListAV, WatchlistDetailsAV,StreamPlatformAV,
                                     StreamPlatformDetailsAV, ReviewList, ReviewDetail,
                                     ReviewCreate)
urlpatterns = [
    path('', WatchListAV.as_view(), name='movies'),
    path('<int:pk>', WatchlistDetailsAV.as_view(), name='movie_details'),
    path('streams/', StreamPlatformAV.as_view(), name='streams'),
    path('streams/<int:pk>', StreamPlatformDetailsAV.as_view(), name='streamplatform-detail'),

    path('reviews/<int:pk>/create', ReviewCreate.as_view(), name='reviews-create'),
    path('reviews/<int:pk>', ReviewList.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/review', ReviewDetail.as_view(), name='reviews-detail'),
]
