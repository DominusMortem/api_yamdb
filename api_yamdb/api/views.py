from rest_framework import viewsets
from .serializers import CategorySerializer
from titles.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
