from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='api_post_list'),
    path('posts/<slug:slug>/', PostDetailAPIView.as_view(), name='api_post_detail'),
]