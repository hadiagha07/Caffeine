from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    image_file = models.ImageField(upload_to="category/%Y/%m/", blank=True, null=True)
    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Slider(models.Model):
    image = models.ImageField(upload_to="sliders/%Y/%m/", verbose_name='تصویر اسلایدر')
    link = models.URLField(verbose_name='لینک مرتبط')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    english_name = models.CharField(max_length=100, verbose_name='نام انگلیسی محصول')
    price = models.PositiveBigIntegerField(verbose_name='قیمت')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='دسته‌بندی')
    description = models.TextField(verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Feature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE, verbose_name='محصول')
    name = models.CharField(max_length=100, verbose_name='نام ویژگی')
    value = models.CharField(max_length=100, verbose_name='مقدار ویژگی')

    def __str__(self):
        return f"{self.name} - {self.value}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to="products/%Y/%m/", verbose_name='تصویر محصول')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        ordering = ['-created']

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='محصول')
    comment = models.TextField(verbose_name='نظر کاربر')
    rating = models.PositiveSmallIntegerField(verbose_name='امتیاز')
    suggested = models.BooleanField(default=False, verbose_name='پیشنهاد شده')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.product.name} - {self.rating}"