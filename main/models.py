from django.db import models
from django import urls
from django.contrib.postgres import fields as pg_fields

# Create your models here.

# meta model
class Tag(models.Model):
    name = models.SlugField(
        max_length=128, allow_unicode=True, primary_key=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("Tag", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# note model model
class Note(models.Model):
    key = models.SlugField(max_length=128, allow_unicode=True)
    markdown = models.TextField()
    markdown_time = models.DateTimeField()
    draft = models.TextField(blank=True, null=True)
    draft_time = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.key

    def get_absolute_url(self):
        return urls.reverse('note-detail', args=(self.key,))
