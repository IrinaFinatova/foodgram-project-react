from django.db.models import BooleanField, CharField, EmailField
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
#class CustomUserManager(BaseUserManager):
##    """Создание кастомного BaseUserManager
#     с индентификатором вместо username."""
#    def create_user(self, email, password, **extra_fields):
#        """Создание пользователя с e-mail и password"""
#        if not email:
#            raise ValueError('Email должен быть определен')
#        email = self.normalize_email(email)
#        user = self.model(email=email, **extra_fields)
#        user.set_password(password)
#        user.save()
#       return user
#
#    def create_superuser(self, email, password, **extra_fields):
#        """
#        Create and save a SuperUser with the given email and password.
#        """
#        extra_fields.setdefault('is_staff', True)
#       extra_fields.setdefault('is_superuser', True)
#        if extra_fields.get('is_staff') is not True:
#            raise ValueError('Superuser должен атрибут is_staff=True.')
#        if extra_fields.get('is_superuser') is not True:
#            raise ValueError('Superuser должен иметь атрибут is_superuser=True.')
#       return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = EmailField(max_length=254,
                       unique=True,
                       verbose_name='Электронная почта',
                       validators=[EmailValidator(message='Неправильный фофрмат адреса электронной почты!')],
                       error_messages={'unique':
                                           ('Пользователь с таким адресом электронной почты уже существует!')})
    username = CharField(max_length=150,
                         verbose_name='Username',
                         validators=[RegexValidator(regex='^[\w.@+-]+$',
                                                    message='Неправильный формат username]!')])
    first_name = CharField(max_length=150,
                           verbose_name='Имя')
    last_name = CharField(max_length=150,
                          verbose_name='Фамилия')
    password = CharField(max_length=150,
                         verbose_name='Пароль')
    is_staff = BooleanField(default=False,
                            verbose_name='Персонал')
    is_superuser = BooleanField(default=False,
                                verbose_name='superuser')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',
                       'first_name',
                       'last_name',
                       'password',
                       'is_staff',
                       'is_superuser']


    class Meta:
        verbose_name = ('Пользователь')
        verbose_name_plural = ('Пользователи')
        ordering = ['-id']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Подписки'
    )
    subscribed = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='Подписчик'
    )

    def clean(self):
        errors = {}
        if self.user == self.subscribed:
            errors['user'] = ValidationError('На себя подписаться нельзя!')
        if errors:
            raise ValidationError(errors)



    class Meta:
        verbose_name = ('Подписка')
        verbose_name_plural = ('Подписки')
        ordering = ['subscribed']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscribed'],
                name='unique_user_subscribed'
            )
        ]

    def __str__(self):
        return f'{self.last_name} {self.first_name}'