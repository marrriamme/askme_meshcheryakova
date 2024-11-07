from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Count
from django.utils import timezone

class QuestionManager(Manager):
    def new_questions(self):
        return self.order_by('-created_at')

    def best_questions(self):
        return self.annotate(annotated_like_count=Count('questionlike')).order_by('-annotated_like_count')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    objects = QuestionManager()

    @property
    def likes_count(self):
        return self.questionlike_set.count()

    @property
    def answers_count(self):
        return self.answers.count()

    @property
    def tags_list(self):
        return self.tags.all()

    def __str__(self):
        return f"Question: {self.title} by {self.author.user.username}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(default=timezone.now) # Время создания ответа
    is_correct = models.BooleanField(default=False)  # Флаг правильного ответа

    @property
    def likes_count(self):
        return self.answerlike_set.count()

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.author.user.username}"

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"Like by {self.user.user.username} for question '{self.question.title}'"

class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"Like by {self.user.user.username} for answer on '{self.answer.question.title}'"
