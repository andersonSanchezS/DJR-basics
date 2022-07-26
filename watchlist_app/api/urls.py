
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchListAV, WatchlistDetailsAV,StreamPlatformVS,
                                     StreamPlatformDetailsAV, ReviewList, ReviewDetail,
                                     ReviewCreate)

router = DefaultRouter()
router.register('streams', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movies'),
    path('<int:pk>', WatchlistDetailsAV.as_view(), name='movie_details'),
    path('', include(router.urls)),

    path('<int:pk>/create', ReviewCreate.as_view(), name='reviews-create'),
    path('<int:pk>/review', ReviewList.as_view(), name='reviews-list'),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='reviews-detail'),
]
