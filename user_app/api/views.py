# REST Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Serializers Imports
from .serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    def post(self, request):
        try:
            # Data response dict
            data = {}
            # Serializer instance
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            # Setting the data response
            data['email'] = account.email
            data['username'] = account.username
            data['response'] = 'Successfully registered.'
            # Generating the JWT
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
