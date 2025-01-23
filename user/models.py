from django_jalali.db import models as jmodels
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
import phonenumbers
from django.core.exceptions import ValidationError


def validate_iranian_phone(value):
    try:
        phone = phonenumbers.parse(value, "IR")
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError('شماره تلفن معتبر نیست')
    except:
        raise ValidationError('قالب شماره تلفن نادرست است')


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        """
        ایجاد کاربر عادی با شماره تلفن و پسورد
        """
        if not phone:
            raise ValueError('شماره تلفن الزامی است')

        # اعتبارسنجی پیشرفته شماره تلفن
        try:
            phone = phonenumbers.parse(phone, "IR")
            if not phonenumbers.is_valid_number(phone):
                raise ValueError('شماره تلفن معتبر نیست')
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)
        except phonenumbers.NumberParseException:
            raise ValueError('قالب شماره تلفن نادرست است')

        user = self.model(
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """
        ایجاد سوپریوزر با دسترسی کامل
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپریوزر باید is_staff=True داشته باشد')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('سوپریوزر باید is_superuser=True داشته باشد')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    مدل کاربری سفارشی با احراز هویت مبتنی بر شماره تلفن
    """
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_iranian_phone],
        verbose_name='شماره تلفن',
        help_text='مثال: ۰۹۱۲۳۴۵۶۷۸۹'
    )
    first_name = models.CharField(
        max_length=25,
        verbose_name='نام',
        blank=True
    )
    last_name = models.CharField(
        max_length=25,
        verbose_name='نام خانوادگی',
        blank=True
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='آخرین IP ورود'
    )
    joined = jmodels.jDateTimeField(
        default=timezone.now,
        verbose_name='تاریخ عضویت'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='دسترسی ادمین'
    )
    profile_image = models.ImageField(
        upload_to="users/profiles/%Y/%m/",
        verbose_name='تصویر پروفایل',
        blank=True,
        default='default_profile.png'
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.get_full_name()} ({self.phone})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name.strip()

    def clean(self):
        # نرمال سازی شماره تلفن
        try:
            phone = phonenumbers.parse(self.phone, "IR")
            self.phone = phonenumbers.format_number(
                phone,
                phonenumbers.PhoneNumberFormat.NATIONAL
            ).replace(' ', '')
        except:
            pass
