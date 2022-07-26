# Django Imports
from django.shortcuts import get_object_or_404
# Rest Framework Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
# Model Imports
from watchlist_app.models import WatchList, StreamPlatform, Review
# Serializer Imports
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
# Permission Imports
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly


class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(pk=pk)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie')

        if movie.avg_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2

        movie.num_ratings = movie.num_ratings + 1

        movie.save()

        serializer.save(watchlist=movie, review_user=review_user)


class StreamPlatformAV(APIView):
    @staticmethod
    def get(request):
        try:
            data = StreamPlatform.objects.all()
            serializer = StreamPlatformSerializer(data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request):
        try:
            data = StreamPlatformSerializer(data=request.data)
            if data.is_valid():
                data.save()
                return Response(data.data, status=status.HTTP_201_CREATED)
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailsAV(APIView):
    @staticmethod
    def get(request, pk):
        try:
            data = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(data, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        try:
            data = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        try:
            data = StreamPlatform.objects.get(pk=pk)
            data.delete()
            return Response({'Success': 'Deleted'}, status=status.HTTP_200_OK)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]

    @staticmethod
    def get(request):
        try:
            data = WatchList.objects.all()
            serializer = WatchListSerializer(data, many=True)
            return Response(serializer.data)
        except WatchList.doesNotExist:
            return Response({'Error': 'No records'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def post(request):
        try:
            serializer = WatchListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WatchlistDetailsAV(APIView):

    @staticmethod
    def get(request, pk):
        try:
            data = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(data)
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def put(request, pk):
        try:
            data = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete(request, pk):
        try:
            data = WatchList.objects.get(pk=pk)
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
