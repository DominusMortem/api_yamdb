from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=False)
    year = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
