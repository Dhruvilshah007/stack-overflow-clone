# Generated by Django 3.1.7 on 2021-11-20 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionsApp', '0005_auto_20211120_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_status',
            field=models.CharField(choices=[('Solved', 'Solved'), ('Not Solved', 'Not Solved')], default='Not Solved', max_length=20),
        ),
    ]
