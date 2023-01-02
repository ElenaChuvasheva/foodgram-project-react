# Generated by Django 2.2.16 on 2023-01-01 09:09

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_ordering'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='author_not_user_constraint'),
        ),
    ]
