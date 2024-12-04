from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Count, F
from django.utils import timezone
from datetime import timedelta
from django.templatetags.static import static


class QuestionManager(Manager):
    def new_questions(self):
        return self.order_by('-created_at')

    def best_questions(self):
        return self.annotate(annotated_like_count=Count('questionlike')).order_by('-annotated_like_count')

class AnswerManager(Manager):
    def best_answers(self):
        return self.annotate(annotated_like_count=Count('answerlike')).order_by('-annotated_like_count')
    
class TagManager(Manager):
    def best_tags(self):
        return self.annotate(question_count=Count('questions')).order_by('-question_count')[:20]
    
# class BestMemberManager(Manager):
#     def best_members(self):
#         one_week_ago = timezone.now() - timedelta(weeks=1)

#         recent_questions = Question.objects.filter(created_at__gte=one_week_ago)
#         recent_answers = Answer.objects.filter(created_at__gte=one_week_ago)

#         combined_posts = list(recent_questions) + list(recent_answers)
#         combined_posts = sorted(combined_posts, key=lambda post: post.likes_count, reverse=True)[:10]

#         authors = {post.author.id for post in combined_posts}
#         profiles = Profile.objects.filter(id__in=authors)

#         sorted_profiles = sorted(profiles, key=lambda profile: self.get_popularity_score(profile, combined_posts), reverse=True)
#         return sorted_profiles[:10]

#     def get_popularity_score(self, profile, combined_posts):
#         popularity_score = 0
#         for post in combined_posts:
#             if post.author == profile:
#                 popularity_score += post.likes_count

#         return popularity_score

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/avatars/', null=True, blank=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    # objects = BestMemberManager()

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('avatars/ava.jpg') 

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
    
    @property
    def author_avatar_url(self):
        if self.author.avatar:
            return self.author.avatar.url
        return static('avatars/ava.jpg')

    def __str__(self):
        return f"Question: {self.title} by {self.author.user.username}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(default=timezone.now) 
    is_correct = models.BooleanField(default=False)  
    objects = AnswerManager()

    @property
    def likes_count(self):
        return self.answerlike_set.count()
    
    @property
    def author_avatar_url(self):
        if self.author.avatar:
            return self.author.avatar.url
        return static('avatars/ava.jpg')

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.author.user.username}"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    objects = TagManager()

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
