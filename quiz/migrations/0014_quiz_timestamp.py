# Generated by Django 4.2.7 on 2023-11-13 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_option_qn_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
