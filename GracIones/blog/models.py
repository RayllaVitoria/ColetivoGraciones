import re
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from easy_thumbnails.fields import ThumbnailerImageField
from django.core import validators
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Post(models.Model):
    capa = ThumbnailerImageField(
        upload_to="capa",
        blank=True,
        resize_source=dict(size=(215, 215), crop=True)
    )
    title = models.CharField('Título', max_length=200)
    text = models.TextField('Texto')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('blog:post_list')

    def delete(self):
        self.capa.delete()
        return super(Post, self).delete()   

    def __str__(self):
        return self.title