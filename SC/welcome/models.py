from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.safestring import mark_safe
from django.utils import timezone
from PIL import Image


class Club(User):
    """
    Database model of Science Club user
    """
    class Meta:
        verbose_name = 'Science Club'
        verbose_name_plural = 'Science Clubs'

    sc_name = models.CharField("Science Club Name", max_length=1000, unique=True)
    phone_number = models.CharField(max_length=17, blank=True)
    profile_image = models.ImageField(upload_to='uploads/club/profile_image', default="uploads/club/profile_image/default_profile.jpg", blank=True)  # 300x300
    background_image = models.ImageField(upload_to='uploads/club/background_image', default="uploads/club/background_image/default_background.png", blank=True)  # 2000x400
    about = models.CharField(max_length=5000, default="", blank=True)
    token = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return self.sc_name

    def save(self, *args, **kwargs):
        super(Club, self).save(*args, **kwargs)
        profile_image = Image.open(self.profile_image.path)
        size = (300, 300)
        profile_image = profile_image.resize(size, Image.ANTIALIAS)
        profile_image.save(self.profile_image.path)
        background_image = Image.open(self.background_image.path)
        size = (2000, 400)
        background_image = background_image.resize(size, Image.ANTIALIAS)
        background_image.save(self.background_image.path)


class Project(models.Model):
    """
    Database model of user project
    """
    parent = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="Science Club")
    title = models.CharField("Project title", max_length=400)
    about = models.CharField(max_length=5000)
    image = models.ImageField(upload_to='uploads/club/project_image', blank=True)  # 900x600
    active = models.BooleanField()
    start_date = models.DateField(blank=True, default=timezone.now)
    deadline = models.DateField(blank=True, default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        imag = Image.open(self.image.path)
        size = (900, 600)
        imag = imag.resize(size, Image.ANTIALIAS)
        imag.save(self.image.path)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 200px; height:200px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'


class Post(models.Model):
    """
    Databace model of user post
    """
    parent = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="Science Club")
    title = models.CharField("Post title", max_length=400)
    image = models.ImageField(upload_to='uploads/club/post_image', blank=True)  # 900x600
    contents = models.CharField(max_length=5000)
    publication_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        imag = Image.open(self.image.path)
        size = (900, 600)
        imag = imag.resize(size, Image.ANTIALIAS)
        imag.save(self.image.path)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 200px; height:200px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'


