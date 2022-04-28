from django.urls import include, path
from rest_framework import routers
from .views import CategoryViewSet, GenresViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
]
