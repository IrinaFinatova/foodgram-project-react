from django.db.models import BooleanField, CharField, EmailField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Создание кастомного BaseUserManager
     с индентификатором вместо username."""
    def create_user(self, email, password, **extra_fields):
        """Создание пользователя с e-mail и password"""
        if not email:
            raise ValueError('Email должен быть определен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен атрибут is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь атрибут is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = EmailField(max_length=254,
                       unique=True,
                       verbose_name='Электронная почта')
    username = CharField(max_length=150,
                         verbose_name='Username')
    first_name = CharField(max_length=150,
                           verbose_name='Имя')
    last_name = CharField(max_length=150,
                          verbose_name='Фамилия')
    password = CharField(max_length=150,
                         verbose_name='Пароль')
    is_subscribed = BooleanField(default=False,
                                 verbose_name='Подписан')
    is_staff = BooleanField(verbose_name='Персонал')
    is_superuser = BooleanField(verbose_name='superuser')

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = ('Пользователь')
        verbose_name_plural = ('Пользователи')
        ordering = ['-id']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'