# Generated by Django 2.2.16 on 2023-01-01 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='not_banned',
            field=models.BooleanField(default=True, verbose_name='Не забанен'),
        ),
    ]
