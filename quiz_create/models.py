from django.db import models

# Create your models here.

from django.db import models

class Quiz(models.Model):
    class Category(models.TextChoices):
        SCIENCE = 'SCI', 'Science'
        HISTORY = 'HIS', 'History'
        SPORT = 'SPT', 'Sport'
        MATH = 'MTH', 'Math'
        COMEDY = 'CMD', 'Comedy'
        GAMES = 'GMS', 'Games'
        EDUCATION = 'EDU', 'Education'
        OTHER = 'OTH', 'Other'

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    title = models.CharField(max_length=30)
    content = models.TextField()
    correct_answer = models.CharField(max_length=20)
    incorrect1 = models.CharField(max_length=20)
    incorrect2 = models.CharField(max_length=20)
    incorrect3 = models.CharField(max_length=20)
    explanation = models.TextField(max_length=50)

