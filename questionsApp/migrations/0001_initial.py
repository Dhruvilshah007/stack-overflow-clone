# Generated by Django 3.1.7 on 2021-11-19 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_title', models.CharField(default='', max_length=100)),
                ('question_body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('question_status', models.CharField(max_length=15, null=True)),
                ('question_tags', models.CharField(default='', max_length=100)),
                ('question_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]