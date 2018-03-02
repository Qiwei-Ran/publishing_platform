from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import IsSuperUser
from perms.auth_handle import auth_dict_class
from serializers import DepartmentModeSerializer, CustomUserSerializer
from users.models import CustomUser
from users.models import DepartmentMode
from utils.users_token import generate_token
from utils.paginator import Paginator

'''
class DepartmentModeListApi(generics.ListAPIView):
    queryset = DepartmentMode.objects.all()
    serializer_class = DepartmentModeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
'''


class UserToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if not request.user.is_authenticated:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            data = CustomUser.objects.get(username=username)
            check_data = check_password(password, data.password)

            if check_data:
                user = data
                token = generate_token(request, user)
                return Response({'Token': token, 'Keyword': 'Bearer'}, status=200)
            else:
                msg = None
                return Response({'error': msg}, status=406)
        else:
            user = request.user
            msg = None
            token = generate_token(request, user)
            return Response({'Token': token, 'Keyword': 'Bearer'}, status=200)


class DepartmentModeViewSet(viewsets.ModelViewSet):
    """General ViewSet contain basic CURD"""
    queryset = DepartmentMode.objects.all()
    serializer_class = DepartmentModeSerializer
    filter_fields = '__all__'
    permission_classes = (IsSuperUser,)


class DepartmentModeUpdateApi(generics.RetrieveUpdateAPIView):
    """Update DepartmentMode Fields"""
    queryset = DepartmentMode.objects.all()
    serializer_class = DepartmentModeSerializer
    permission_classes = (IsSuperUser,)


class UserViewSet(viewsets.ModelViewSet):
    """This is user model"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUser,)


class UserProfile(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Get current user profile
        :param request:
        :return: the profile
        """
        return Response(request.user.to_json())

    def post(self, request):
        return Response(request.user.to_json())
