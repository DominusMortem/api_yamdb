from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, MyTokenView, SignUpViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('auth/signup', SignUpViewSet, basename='signup')


urlpatterns = [
    path('v1/auth/token/', MyTokenView.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
