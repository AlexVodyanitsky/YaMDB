from django.urls import include, path
from rest_framework import routers

from .categories_and_more.views import (CategoryViewSet, GenreViewSet,
                                        TitleViewSet)
from .reviews.views import CommentViewSet, ReviewViewSet
from .users.views import GetTokenView, SignUpView, UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)
v1_router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token_obtain_pair'),
    path('v1/', include(v1_router.urls)),
]
