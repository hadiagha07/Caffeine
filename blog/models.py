from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from user.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='posts/', blank=True)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=300, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']
