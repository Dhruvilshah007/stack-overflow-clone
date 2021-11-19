# Generated by Django 3.1.7 on 2021-11-19 17:27

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('questionsApp', '0003_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_body',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_body',
            field=tinymce.models.HTMLField(),
        ),
    ]
