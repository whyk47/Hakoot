# Generated by Django 4.2.7 on 2023-11-12 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_question_qn_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='desc',
            field=models.CharField(default='', max_length=512),
        ),
    ]