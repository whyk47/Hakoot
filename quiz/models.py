from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    pass


class Quiz(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    name = models.CharField(max_length=128)
    desc = models.CharField(max_length=512, default="")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def num_questions(self):
        return self.questions.all().count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=512)
    qn_no = models.IntegerField(default=1, validators=[
        MinValueValidator(0)
    ])
    correct_option = models.IntegerField(default=0, choices=(
        (i - 1, i) for i in range(1, 5)
    ))
    time_limit = models.IntegerField(default=30, choices=(
        (i * 10, i * 10) for i in range(1, 7)
    ))


class Option(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="options")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    qn_no = models.IntegerField(default=1, validators=[
        MinValueValidator(0)
    ])
    option = models.CharField(max_length=512)
    option_no = models.IntegerField(default=1)


class Quiz_attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def score(self):
        return sum([attempt.score() for attempt in self.qn_attempts.all()])
    
    def current_question(self):
        return self.qn_attempts.count()
    
class Question_attempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempts")
    option_chosen = models.IntegerField(default=-1)
    quiz_attempt = models.ForeignKey(Quiz_attempt, on_delete=models.CASCADE, related_name="qn_attempts")
    time_left = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)

    def correct(self):
        return int(self.question.correct_option) == int(self.option_chosen)
    
    def score(self):
        if self.correct():
            return int(500 + 500 * (self.time_left / self.question.time_limit))
        else:
            return 0