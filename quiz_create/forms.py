from django import forms
from .models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'category',
            'title',
            'description',
            'content',
            'correct_answer',
            'incorrect1',
            'incorrect2',
            'incorrect3',
            'explanation',
        ]