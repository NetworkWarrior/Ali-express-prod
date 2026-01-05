from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
# Create your models here.


class Operator(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE, default=None)
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Topic(models.Model):
    name = models.CharField(max_length=200)
    picture_url = models.URLField(default="http://buprof.com/wp-content/uploads/2016/01/konular.png", blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"({self.topic}) {self.title}"

    class Meta:
        ordering = ['-created_at']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

