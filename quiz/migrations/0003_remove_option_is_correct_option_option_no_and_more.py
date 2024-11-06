# Generated by Django 4.2.7 on 2023-11-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quiz_question_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='option',
            name='option_no',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_option',
            field=models.IntegerField(default=1),
        ),
    ]