from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    image_file = models.ImageField(upload_to="uploads/%Y/%m/", blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name

    class Slider(models.Model):
        slider = models.ImageField(upload_to="uploads/%Y/%m/")
        link = models.URLField()
        created = models.DateTimeField(auto_now_add=True)

        class Meta:
            verbose_name = 'اسلایدر'
            verbose_name_plural = 'اسلایدرها'



class Product(models.Model):
    nickname = models.CharField(max_length=100, verbose_name='اسم محصول به انگلیسی')
    name = models.CharField(max_length=100, verbose_name='اسم محصول')
    price = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name


class Feature(models.Model):
    product = models.ForeignKey(Product, verbose_name='محصول', related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='اسم ویزگی')
    value = models.CharField(max_length=100, verbose_name='ولیو ویزگی')

    def __str__(self):
        return f"{self.name}: {self.value}"


class Image(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    image_file = models.ImageField(upload_to="uploads/%Y/%m/", blank=True, null=True, verbose_name='فایل تصویر')
    created = models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد')


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    suggested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name}"