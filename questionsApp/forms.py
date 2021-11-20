from django import forms
from .models import Question


class Question_Form(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            'question_title',
            'question_body',
            'question_status',
            'question_tags'
        )
        widgets = {
            'question_tags': forms.CheckboxSelectMultiple(),
            'question_title': forms.TextInput(attrs={'class': 'form-control'})

        }
