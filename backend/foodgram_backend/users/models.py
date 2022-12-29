from django.contrib.auth.models import AbstractUser
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
        default=USER
    )
    subscribed_to = models.ManyToManyField(
        'CustomUser',
        verbose_name='Подписки',
        related_name='subscribers',
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN
        super(CustomUser, self).save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == self.ADMIN


@receiver(m2m_changed, sender=CustomUser.subscribers.through)
def prevent_duplicate_tags_from_group(sender, instance, action,
                                      reverse, model, pk_set, **kwargs):
    if action == 'pre_add':
        if instance.pk in pk_set:
            raise ValidationError({'Нельзя подписаться на себя'})
