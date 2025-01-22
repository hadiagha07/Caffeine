from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from shop.models import Category, Product, Slider, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    SliderSerializer,
    ReviewSerializer
)


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




class HomeAPIView(BaseAPIView):
    def get(self, request):
        popular_categories = Category.objects.order_by('-views')[:5]
        latest_products = Product.objects.order_by('-created')
        special = Product.objects.filter(product_type='شگفت انگیز')