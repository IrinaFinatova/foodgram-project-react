from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models import CharField, EmailField


class CustomUser(AbstractUser):
    email = EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        validators=[
            EmailValidator(
                message='Неправильный фофрмат адреса электронной почты!')],
        error_messages={
            'unique':
            ('Пользователь с таким адресом электронной почты уже существует')})
    username = CharField(
        max_length=150,
        verbose_name='Username',
        validators=[RegexValidator(regex='^[\w.@+-]+$',
                    message='Неправильный формат username]!')])
    first_name = CharField(max_length=150,
                           verbose_name='Имя')
    last_name = CharField(max_length=150,
                          verbose_name='Фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',
                       'first_name',
                       'last_name']

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
        related_name='subscrib',
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
        return f'{self.subscribed.last_name} {self.user.last_name}'
