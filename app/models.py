from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Count, F
from django.utils import timezone
from datetime import timedelta
from django.templatetags.static import static
from django.db.models import Q, F, Count


class Image(models.Model):
    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to="images")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def file_url(self):
        return self.file.url

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_at')

    def best_questions(self):
        return self.annotate(
            annotated_like_count=Count('questionlike', filter=Q(questionlike__like_type='like')),
            annotated_dislike_count=Count('questionlike', filter=Q(questionlike__like_type='dislike'))
        ).annotate(
            like_dislike_diff=F('annotated_like_count') - F('annotated_dislike_count')
        ).order_by('-like_dislike_diff')


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
    avatar = models.OneToOneField(Image, on_delete=models.SET_NULL, blank=True, null=True)  
    nickname = models.CharField(max_length=100, blank=True, null=True)
    # objects = BestMemberManager()

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def avatar_url(self):
        if self.avatar and self.avatar.file:
            return self.avatar.file.url
        return static('avatars/ava.jpg')

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    objects = QuestionManager()

    @property
    def rating(self):
        likes = self.questionlike_set.filter(like_type='like').count()
        dislikes = self.questionlike_set.filter(like_type='dislike').count()
        return likes - dislikes

    @property
    def answers_count(self):
        return self.answers.count()
    
    @property
    def tags_list(self):
        return self.tags.all()
    
    def is_liked_by_user(self, user):
        if user.is_authenticated:
            return self.questionlike_set.filter(user=user.profile, like_type=LikeType.LIKE).exists()
        return False

    def is_disliked_by_user(self, user):
        if user.is_authenticated:
            return self.questionlike_set.filter(user=user.profile, like_type=LikeType.DISLIKE).exists()
        return False

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
    def rating(self):
        likes = self.answerlike_set.filter(like_type='like').count()
        dislikes = self.answerlike_set.filter(like_type='dislike').count()
        return likes - dislikes
    
    def is_liked_by_user(self, user):
        if user.is_authenticated:
            return self.answerlike_set.filter(user=user.profile, like_type=LikeType.LIKE).exists()
        return False

    def is_disliked_by_user(self, user):
        if user.is_authenticated:
            return self.answerlike_set.filter(user=user.profile, like_type=LikeType.DISLIKE).exists()
        return False

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.author.user.username}"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    objects = TagManager()

    def __str__(self):
        return self.name

class LikeType(models.TextChoices):
    LIKE = 'like', 'Like'
    DISLIKE = 'dislike', 'Dislike'

class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like_type = models.CharField(
        max_length=7, choices=LikeType.choices, default=LikeType.LIKE
    )

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.get_like_type_display()} by {self.user.user.username} for question '{self.question.title}'"

class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    like_type = models.CharField(
        max_length=7, choices=LikeType.choices, default=LikeType.LIKE
    )

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.get_like_type_display()} by {self.user.user.username} for answer on '{self.answer.question.title}'"
