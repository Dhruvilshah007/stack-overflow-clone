from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=100, default="")
    question_body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    question_status = models.CharField(max_length=15, null=True)
    question_tags = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.question_title
