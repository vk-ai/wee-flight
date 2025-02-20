from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from social_django.utils import load_strategy, load_backend
from .serializers import SocialAuthSerializer, UserSerializer
import jwt
import os

class SocialAuthView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.validated_data.get('provider')
        access_token = serializer.validated_data.get('access_token')

        strategy = load_strategy(request)
        
        try:
            backend = load_backend(strategy=strategy, name=provider,
                                 redirect_uri=None)
            user = backend.do_auth(access_token)

            if user:
                token = jwt.encode(
                    {
                        'user_id': user.id,
                        'email': user.email,
                    },
                    os.getenv('JWT_SECRET_KEY'),
                    algorithm='HS256'
                )
                
                return Response({
                    'token': token,
                    'user': UserSerializer(user).data
                })
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)