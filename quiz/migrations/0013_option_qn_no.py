# Generated by Django 4.2.7 on 2023-11-13 00:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_alter_option_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='qn_no',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]