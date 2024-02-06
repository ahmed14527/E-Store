from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login, logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.contrib.auth.models import User


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_description="User registration API",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                # Add more properties as needed
                            },
                        ),
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: 'Bad Request',
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=AuthTokenSerializer,
        operation_description="User login API",
        responses={
            200: 'OK',
            400: 'Bad Request',
        },
    )
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class LogoutView(APIView):
    @swagger_auto_schema(
        operation_description="User logout API",
        responses={
            200: openapi.Response(description="OK"),
        },
    )
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response({"details": "Successfully logged out"}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Get all users API",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'username': openapi.Schema(type=openapi.TYPE_STRING),
                            # Add more properties as needed
                        },
                    ),
                ),
            ),
            400: 'Bad Request',
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
    
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

@swagger_auto_schema(method='GET', operation_summary='User Profile', responses={200: 'OK'})
@api_view(['GET'])
def user_profile(request):
    """
    Retrieve the user profile.
    """
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
    }
    return Response(data)
    