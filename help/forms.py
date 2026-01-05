from django import forms
from .models import Question, Answer


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'description', 'picture')
        widgets = {
            'picture': forms.ClearableFileInput()  # remove multiple

        }
        labels = {
            'picture': 'Upload a picture (optional)',
        }
        required = {
            'picture': False,
        }


class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('description',)



