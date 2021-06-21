from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core import validators

User = get_user_model()

class Community(models.Model):
    owner = models.ForeignKey(User, related_name='own_communities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    description = models.TextField(null=True)
    password = models.CharField(max_length=100, null=False, validators=[validators.MinLengthValidator(8, 'Please enter at least 8 charactors')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Community#{self.id}-{self.name}'

    def save(self, **kwargs):
        self.password = make_password(self.password, None, 'md5')
        super().save(**kwargs)

class Resident(models.Model):
    owner = models.ForeignKey(User, related_name='own_residents', on_delete=models.CASCADE)
    community = models.ForeignKey(Community, related_name='residents', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=False, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.community}'

class VideoGroup(models.Model):
    community = models.ForeignKey(Community, related_name='video_groups', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    community = models.ForeignKey(Community, related_name='videos', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(VideoGroup, related_name='videos', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    resident_posted = models.ForeignKey(Resident, related_name='posts', on_delete=models.CASCADE, null=True)
    user_posted = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null=True)
    posted_to = models.ForeignKey(Video, related_name='posts', on_delete=models.CASCADE)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'post#{self.id}'

class Comment(models.Model):
    resident_commented = models.ForeignKey(Resident, related_name='comments', on_delete=models.CASCADE, null=True)
    user_commented = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=True)
    commented_to = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment#{self.id}'