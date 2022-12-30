from django.contrib.auth.models import AbstractUser, Permission
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from utils.strings import LowerCaseEmailField
from utils.validators import MaxLengthValidatorMessage


class CustomUser(AbstractUser):
    """Кастомная модель User."""
    ADMIN = 'admin'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[
            MaxLengthValidatorMessage(150),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Используйте буквы, цифры, знаки ., @, +, -'
            ),
        ],
        verbose_name='Nickname пользователя',
    )
    email = LowerCaseEmailField(
        max_length=254,
        unique=True,
        validators=[MaxLengthValidatorMessage(254)],
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        validators=[MaxLengthValidatorMessage(150)],
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        validators=[MaxLengthValidatorMessage(150)],
        verbose_name='Фамилия пользователя'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )
#    subscribed_to = models.ManyToManyField(
#        'CustomUser',
#        verbose_name='Подписки',
#        related_name='subscribers',
#        blank=True
#    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == self.ADMIN:
            self.is_staff = True
        if self.is_superuser:
            self.role = self.ADMIN
        super(CustomUser, self).save(*args, **kwargs)
        if self.is_admin and not self.is_superuser:
            self.add_admin_permissions()

    def add_admin_permissions(self):
        ingredient_perms = Permission.objects.filter(
            content_type__model='ingredienttype'
        )
        ingredientamount_perms = Permission.objects.filter(
            content_type__model='ingredientamount')
        tag_perms = Permission.objects.filter(
            content_type__model='tag')
        recipe_perms = Permission.objects.filter(
            content_type__model='recipe').exclude(codename='add_recipe')
        user_perms = Permission.objects.filter(
            content_type__model='customuser')
        subscribe_perms = Permission.objects.filter(
            content_type__model='subscribe').exclude(codename='add_subscribe')
        self.user_permissions.add(*ingredient_perms, *ingredientamount_perms,
                                  *recipe_perms, *subscribe_perms,
                                  *tag_perms, *user_perms)

    @property
    def is_admin(self):
        return self.role == self.ADMIN


#@receiver(m2m_changed, sender=CustomUser.subscribers.through)
#def prevent_duplicate_tags_from_group(sender, instance, action,
#                                      reverse, model, pk_set, **kwargs):
#    if action == 'pre_add':
#        if instance.pk in pk_set:
#            raise ValidationError({'Нельзя подписаться на себя'})
