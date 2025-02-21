# Generated by Django 5.1.4 on 2025-01-23 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sliders/%Y/%m/', verbose_name='تصویر اسلایدر')),
                ('link', models.URLField(verbose_name='لینک مرتبط')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'اسلایدر',
                'verbose_name_plural': 'اسلایدرها',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='نام دسته\u200cبندی')),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='category/%Y/%m/')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')),
            ],
            options={
                'verbose_name': 'دسته\u200cبندی',
                'verbose_name_plural': 'دسته\u200cبندی\u200cها',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='shop_catego_name_289c7e_idx')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('شگفت انگیز', 'شگفت انگیز'), ('عادی', 'عادی')], default='عادی', max_length=50, verbose_name='نوع محصول')),
                ('name', models.CharField(max_length=100, verbose_name='نام محصول')),
                ('english_name', models.CharField(max_length=100, verbose_name='نام انگلیسی محصول')),
                ('price', models.PositiveBigIntegerField(verbose_name='قیمت')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='دسته\u200cبندی')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام ویژگی')),
                ('value', models.CharField(max_length=100, verbose_name='مقدار ویژگی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='shop.product', verbose_name='محصول')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/%Y/%m/', verbose_name='تصویر محصول')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product', verbose_name='محصول')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='نظر کاربر')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='امتیاز')),
                ('suggested', models.BooleanField(default=False, verbose_name='پیشنهاد شده')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.product', verbose_name='محصول')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
