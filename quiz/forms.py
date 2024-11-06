from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'correct_option', 'time_limit', 'qn_no']
        labels = {
            "time_limit": "Time Limit (s)"
        }
        widgets = {
            "qn_no": forms.HiddenInput()
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option', 'qn_no']
        labels = {
            "option": ""
        }
        widgets = {
            "qn_no": forms.HiddenInput()
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'desc']
        widgets = {
            "desc": forms.Textarea(attrs={'rows': 3})
        }
