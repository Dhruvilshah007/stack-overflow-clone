from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField

# Create your models here.


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=30)

    def __str__(self):
        return self.tag_name


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=100, default="")
    question_body = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    question_status = models.CharField(max_length=15, null=True)
    question_tags = models.ManyToManyField(Tags)

    def __str__(self):
        return str(self.question_id)


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    answer_body = RichTextField(blank=True, null=True)
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answering = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.answer_id)
