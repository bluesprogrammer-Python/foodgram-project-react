from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowUserSerializer, UserSerializer

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowUserSerializer(page, many=True,
                                          context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({'errors':
                            ('Нельзя подписаться на самого себя.')},
                            status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(user=user, author=author)
        queryset = Follow.objects.get(user=request.user, author=author)
        serializer = FollowUserSerializer(queryset,
                                          context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if not Follow.objects.filter(user=user, author=author).exists():
            return Response({'errors': 'Подписки не существует.'},
                            status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.get(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


