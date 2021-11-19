# Generated by Django 3.1.7 on 2021-11-19 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionsApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_tags',
        ),
        migrations.AddField(
            model_name='question',
            name='question_tags',
            field=models.ManyToManyField(to='questionsApp.Tags'),
        ),
    ]