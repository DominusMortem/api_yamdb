from django.urls import include, path
from rest_framework import routers
from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
]