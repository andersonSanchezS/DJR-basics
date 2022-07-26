from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(pk=pk)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk)
        serializer.save(watchlist=movie)

'''

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class ReviewList(generics.GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
'''


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
