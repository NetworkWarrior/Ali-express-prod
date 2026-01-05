from django.contrib import admin
from .models import Operator, Topic, Question, Answer
# Register your models here.

admin.site.register(Operator)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)


