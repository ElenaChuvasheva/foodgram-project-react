from django.contrib.auth.models import AbstractUser, Permission
from django.core.validators import RegexValidator
from django.db import models

from utils.strings import LowerCaseEmailField

MAX_LENGTH = 150
MAX_LENGTH_EMAIL = 254


class CustomUser(AbstractUser):
    """Кастомная модель User."""
    username = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Используйте буквы, цифры, знаки ., @, +, -'
            ),
        ],
        verbose_name='Nickname пользователя',
    )
    email = LowerCaseEmailField(
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Фамилия пользователя'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True
        if not self.is_active:
            self.is_staff = False
            self.is_superuser = False
        super(CustomUser, self).save(*args, **kwargs)
        if self.is_staff and not self.is_superuser:
            self.add_admin_permissions()

    def add_admin_permissions(self):
        measure_perms = Permission.objects.filter(
            content_type__model='measure'
        )
        ingredient_perms = Permission.objects.filter(
            content_type__model='ingredienttype'
        )
        ingredientamount_perms = Permission.objects.filter(
            content_type__model='ingredientamount')
        tag_perms = Permission.objects.filter(
            content_type__model='tag')
        recipe_perms = Permission.objects.filter(
            content_type__model='recipe')
        user_perms = Permission.objects.filter(
            content_type__model='customuser'
        )
        subscribe_perms = Permission.objects.filter(
            content_type__model='subscribe')
        self.user_permissions.add(*measure_perms, *ingredient_perms,
                                  *ingredientamount_perms,
                                  *recipe_perms, *subscribe_perms,
                                  *tag_perms, *user_perms)
