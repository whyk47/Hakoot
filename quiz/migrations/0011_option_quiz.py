# Generated by Django 4.2.7 on 2023-11-12 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_remove_option_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='quiz.quiz'),
        ),
    ]
