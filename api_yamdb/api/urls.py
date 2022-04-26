from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, MyTokenView

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', MyTokenView.as_view(), name='MyTokenView'),
]
