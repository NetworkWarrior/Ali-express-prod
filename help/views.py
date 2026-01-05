from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Topic, Question, Operator
from .forms import CreateQuestionForm, CreateAnswerForm
# Create your views here.


class HelpCenterView(View):
    def get(self, request):
        topics = Topic.objects.all()
        return render(request, 'help/help-center.html', {'topics':topics})

class HelpCenterDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        form = CreateQuestionForm()
        answer_form = CreateAnswerForm()
        topic = Topic.objects.get(id=id)
        return render(request, 'help/help-detail.html', {'topic':topic, 'form':form, 'answer_form': answer_form})

    def post(self, request, id):
        form = CreateQuestionForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            topic = Topic.objects.get(id=id)
            question = form.save(commit=False)
            question.topic = topic
            question.user = request.user
            question.save()
            picture = request.FILES.get('picture')
            if picture is not None:
                question.picture.save(picture.name, picture)

            return redirect('help:help-detail', topic.id)
        else:
            return render(request, 'help/help-detail.html', {'form': form})


class HelpCenterAnswers(View):
    def post(self, request, id):
        answer_form = CreateAnswerForm(data=request.POST)
        if answer_form.is_valid():
            question = Question.objects.get(id=id)
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.operator = Operator.objects.get(id=request.user.id)
            answer.description = request.POST['description']
            answer.save()
            return redirect('help:help-detail', question.topic.id)
        else:
            return render(request, 'help/help-detail.html', {'answer_form': answer_form})


class HelpReportView(View):
    def get(self, request):
        return render(request, 'help/help-reports.html')