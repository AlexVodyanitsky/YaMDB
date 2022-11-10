from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status, viewsets
from rest_framework.decorators import action, APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from .serializers import (GetTokenSerializer, MeSerializer,
                          SignUpSerializer, UserSerializer)
from .utils import get_tokens_for_user, send_code
from ..permissions import IsAdmin


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        code = send_code(email)
        User.objects.get_or_create(
            username=username,
            email=email,
            confirmation_code=code
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class GetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data['confirmation_code']
        if confirmation_code == user.confirmation_code:
            return Response(get_tokens_for_user(user), status.HTTP_200_OK)
        return Response(
            {'conf_code': 'Codes do not match'},
            status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        me = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = MeSerializer(me)
            return Response(serializer.data, status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(me, data=request.data)
            serializer.is_valid(raise_exception=True)
            is_admin = self.request.user.role == 'admin'
            is_superuser = self.request.user.is_superuser
            is_admin_or_superuser = is_admin or is_superuser
            data_role = serializer.validated_data.get('role')
            request_role = self.request.user.role
            role = data_role or request_role
            if not is_admin_or_superuser:
                role = self.request.user.role
            serializer.save(role=role)
            return Response(serializer.data, status.HTTP_200_OK)
