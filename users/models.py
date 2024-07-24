# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return ValidationError(_('Please enter a valid email address.'))

    def create_user(self, email, first_name, last_name, country, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('The Email field must be set'))
        if not first_name:
            raise ValueError(_('The First Name field must be set'))
        if not last_name:
            raise ValueError(_('The Last Name field must be set'))
        if not country:
            raise ValueError(_('The Country field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, country=country, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, country, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(email, first_name, last_name, country, password, **extra_fields)
        user.save(using=self._db)

        return user


AUTH_PROVIDERS = {'email': 'email', 'google': 'google'}


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    country = models.CharField(_('country'), max_length=50)
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)  # is_staff field for superuser
    is_verified = models.BooleanField(_('verified'), default=False)  # new is_verified field
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    auth_provider = models.CharField(_('auth provider'), max_length=50, default=AUTH_PROVIDERS.get('email'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country']

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class OneTimePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(_('otp'), max_length=6)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} passcode "

    class Meta:
        verbose_name = _('one time password')
        verbose_name_plural = _('one time passwords')


class Translation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='translations')
    input_text = models.TextField()
    translated_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Translation by {self.user.email} on {self.created_at}"
