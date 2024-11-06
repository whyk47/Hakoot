# Generated by Django 4.2.7 on 2023-11-12 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_quiz_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='quiz',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='quiz.quiz'),
            preserve_default=False,
        ),
    ]
