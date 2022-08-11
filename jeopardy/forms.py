from django import forms
from django.forms import ModelForm
from .models import Jeopardy, Category, Question

class NewJeopardyForm(ModelForm):
    class Meta:
        model = Jeopardy
        fields = ['subject', 'name']

class NewCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category',]

class NewQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['cluevalue', 'clue', 'answer', 'choiceone', 'choicetwo', 'choicethree']