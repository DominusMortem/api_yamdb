from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404

from .serializers import CategorySerializer, CommentSerializer, ReviewSerializer, GenreSerializer
from titles.models import Category, Genre, Review, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title_or_404(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        title = self.get_title_or_404()
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = self.get_title_or_404()
        serializer.save(
            author=self.request.user,
            title_id=title.id
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    # Тут пока не готово!

    def get_queryset(self):
        title = get_object_or_404(Title, self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

