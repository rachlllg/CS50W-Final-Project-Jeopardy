from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from sqlalchemy import false


# use abstractuser model from django to store default user info in database
class User(AbstractUser):
    pass


# create a Subject model to save all subjects to database
class Subject(models.Model):
    choice = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.choice}"


# create a Jeopardy model to save all Jeopardy games to database
class Jeopardy(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=2000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jeopardy")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


# create a Category model to save all categories of a specific Jeopardy game to database
class Category(models.Model):
    category = models.CharField(max_length=50)
    jeopardy = models.ForeignKey(Jeopardy, on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.jeopardy} : {self.category}"

# create a Question model to save all clues/questions of a specific category of a specific Jeopardy game to database
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    clue = models.CharField(max_length=2000)
    
    class Cluevalue(models.IntegerChoices):
        ONEHUNDRED = 100
        TWOHUNDRED = 200
        THREEHUNDRED = 300
        FOURHUNDRED = 400
        FIVEHUNDRED = 500
    cluevalue = models.IntegerField(choices=Cluevalue.choices)
    answer = models.CharField(max_length=2000)
    choiceone = models.CharField(max_length=2000)
    choicetwo = models.CharField(max_length=2000)
    choicethree = models.CharField(max_length=2000)
    answered = models.BooleanField(default=False)

    class Meta:
        ordering = ['cluevalue']
        
    def __str__(self):
        return f"{self.category} : {self.cluevalue}"
    
