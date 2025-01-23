from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from shop.models import Category, Product, Slider, Review
from .serializers import *




class BaseAPIView(APIView):
    """
    یک کلاس پایه برای مدیریت خطاها و کاهش تکرار کد.
    """
    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({
                "status": False,
                "message": "خطای اعتبارسنجی",
                "errors": str(exc),
            }, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, Exception):
            return Response({
                "status": False,
                "message": "مشکلی پیش آمده، لطفاً دوباره امتحان کنید.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return super().handle_exception(exc)



class PostListCreateAPIView(APIView):
    """
    لیست تمام پستها یا ایجاد پست جدید
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(is_published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(APIView):
    """
    مدیریت پستها (نمایش، آپدیت، حذف)
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return None

    def get(self, request, slug):
        post = self.get_object(slug)
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        post = self.get_object(slug)
        if post and post.author == request.user:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, slug):
        post = self.get_object(slug)
        if post and post.author == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


# class HomeAPIView(BaseAPIView):
#     def get(self, request):
#         popular_categories = Category.objects.order_by('-views')[:5]
#         latest_products = Product.objects.order_by('-created')
#         special = Product.objects.filter(product_type='شگفت انگیز')