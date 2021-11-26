from django.db import models
from django.db.models.deletion import SET_NULL
from users.models import Profile
import uuid

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=SET_NULL)
    title = models.CharField(max_length=200)
    # null for database, blank for django to solve post request
    description = models.TextField(null=True, blank=True)
    # default and upload_to are based on MEDIA_ROOT
    featured_image = models.ImageField(
        null=True, blank=True, upload_to='projects/', default="default.jpg") # search in static dir

    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    pos_ratio = models.IntegerField(default=0, null=True, blank=True)

    # TODO: many to many relationship
    tags = models.ManyToManyField('Tag', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'up vote'),
        ('down', 'down vote'),
    )

    # TODO: one to many relationship
    # CASCADE: when parent is gone, all reviews related to it are deleted
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
