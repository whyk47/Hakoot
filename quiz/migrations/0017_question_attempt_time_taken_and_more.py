# Generated by Django 4.2.7 on 2023-11-22 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_quiz_attempt_question_attempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_attempt',
            name='time_taken',
            field=models.DecimalField(decimal_places=2, default=60.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_option',
            field=models.IntegerField(choices=[(0, 1), (1, 2), (2, 3), (3, 4)], default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='time_limit',
            field=models.IntegerField(choices=[(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60)], default=30),
        ),
    ]