from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, CommentViewSet,
                    GenresViewSet, ReviewViewset)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewset,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
