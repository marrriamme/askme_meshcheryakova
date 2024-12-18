from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Question, Tag, Profile, Answer, QuestionLike, AnswerLike, LikeType
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from app.forms import LoginForm, SignupForm, SettingsForm, AskForm, AnswerForm
from django.http import JsonResponse



def index(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request)

    for question in page.object_list:
        question.is_liked = question.is_liked_by_user(request.user)
        question.is_disliked = question.is_disliked_by_user(request.user)

    return render(request, 'index.html', {
        'questions': page.object_list,
        'page': page,
        **get_common_context()
    })

def hot(request):
    questions = Question.objects.best_questions() 
    page = paginate(questions, request) 

    for question in page.object_list:
        question.is_liked = question.is_liked_by_user(request.user)
        question.is_disliked = question.is_disliked_by_user(request.user)

    return render(request, 'hot.html', {
        'questions': page.object_list,
        'page': page,
        **get_common_context()
    })

def tag(request, tag_name):
    tag_instance = get_object_or_404(Tag, name=tag_name)
    questions = tag_instance.questions.all()
    page = paginate(questions, request)

    for question in page.object_list:
        question.is_liked = question.is_liked_by_user(request.user)
        question.is_disliked = question.is_disliked_by_user(request.user)

    return render(request, 'bender.html', {
        'tag_name': tag_name,
        'questions': page.object_list,
        'page': page,
        **get_common_context()
    })

@login_required
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers_page = paginate(question.answers.all(), request) 
    form = AnswerForm()
    per_page = 10

    is_liked_question = question.is_liked_by_user(request.user)
    is_disliked_question = question.is_disliked_by_user(request.user)

    for answer in answers_page:
        answer.is_liked = answer.is_liked_by_user(request.user)
        answer.is_disliked = answer.is_disliked_by_user(request.user)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user.profile
            answer.save()
            return redirect(f"{reverse('question', args=[question.id])}?page={per_page}#answer-{answer.id}")
    
    return render(request, 'question.html', {
        'question': question,
        'answers': answers_page.object_list,
        'page': answers_page,
        'form': form,
        'is_liked_question': is_liked_question,
        'is_disliked_question': is_disliked_question,
        **get_common_context(),
    })


@login_required
def ask(request):
    form = AskForm()
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(author=request.user.profile) 
            return redirect(request.GET.get('continue', reverse('question', kwargs={'question_id': question.pk})))
    
    return render(request, 'ask.html', {"form": form, **get_common_context()})

def signup(request):
    continue_url = request.GET.get('continue', reverse('index'))
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(continue_url)
    else:
        form = SignupForm() 
    return render(request, 'signup.html', {"form": form, **get_common_context()})

def login(request):
    form = LoginForm
    next_url = request.GET.get('next', reverse('index'))  

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(next_url)
            form.add_error('password', 'Invalid username or password.')
    return render(request, 'login.html', {"form": form, **get_common_context()})

@login_required
def settings(request):
    profile = request.user.profile  
    form = SettingsForm(instance=request.user, profile=profile)  
    continue_url = request.GET.get('continue', reverse('settings'))

    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=request.user, profile=profile)
        if form.is_valid():
            form.save()
            return redirect(continue_url)
    return render(request, 'settings.html', {"form": form, **get_common_context()})


def get_common_context():
    return {
        'tags': Tag.objects.best_tags(),
        # 'members': Profile.objects.best_members()
        'members': Profile.objects.all()[:10]
    }
            
def logout(request):
    auth.logout(request)
    next_url = request.GET.get('next', reverse('index'))
    
    return redirect(next_url)


def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(paginator.num_pages)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


@require_POST
@login_required
def like_question(request, question_id):
    profile = Profile.objects.get(user_id=request.user.id)
    question = Question.objects.get(pk=question_id)

    existing_like = QuestionLike.objects.filter(user=profile, question=question)
    if existing_like.exists():
        if existing_like.first().like_type == LikeType.LIKE:
            existing_like.delete()  
        else:
            existing_like.update(like_type=LikeType.LIKE)  
    else:
        QuestionLike.objects.create(user=profile, question=question, like_type=LikeType.LIKE)

    like_count = QuestionLike.objects.filter(question=question, like_type=LikeType.LIKE).count()
    dislike_count = QuestionLike.objects.filter(question=question, like_type=LikeType.DISLIKE).count()

    rating = like_count - dislike_count  

    return JsonResponse({
        'status': 'success',
        'rating': rating
    })

@require_POST
@login_required
def dislike_question(request, question_id):
    profile = Profile.objects.get(user_id=request.user.id)
    question = Question.objects.get(pk=question_id)

    existing_like = QuestionLike.objects.filter(user=profile, question=question)

    if existing_like.exists():
        if existing_like.first().like_type == LikeType.DISLIKE:
            existing_like.delete()  
        else:
            existing_like.update(like_type=LikeType.DISLIKE)  
    else:
        QuestionLike.objects.create(user=profile, question=question, like_type=LikeType.DISLIKE)

    like_count = QuestionLike.objects.filter(question=question, like_type=LikeType.LIKE).count()
    dislike_count = QuestionLike.objects.filter(question=question, like_type=LikeType.DISLIKE).count()

    rating = like_count - dislike_count  

    return JsonResponse({
        'status': 'success',
        'rating': rating
    })

@require_POST
@login_required
def like_answer(request, answer_id):
    profile = Profile.objects.get(user_id=request.user.id)
    answer = Answer.objects.get(pk=answer_id)

    existing_like = AnswerLike.objects.filter(user=profile, answer=answer)
    if existing_like.exists():
        if existing_like.first().like_type == LikeType.LIKE:
            existing_like.delete()
        else:
            existing_like.update(like_type=LikeType.LIKE)  
    else:
        AnswerLike.objects.create(user=profile, answer=answer, like_type=LikeType.LIKE)

    like_count = AnswerLike.objects.filter(answer=answer, like_type=LikeType.LIKE).count()
    dislike_count = AnswerLike.objects.filter(answer=answer, like_type=LikeType.DISLIKE).count()

    rating = like_count - dislike_count

    return JsonResponse({
        'status': 'success',
        'rating': rating
    })

@require_POST
@login_required
def dislike_answer(request, answer_id):
    profile = Profile.objects.get(user_id=request.user.id)
    answer = Answer.objects.get(pk=answer_id)

    existing_like = AnswerLike.objects.filter(user=profile, answer=answer)

    if existing_like.exists():
        if existing_like.first().like_type == LikeType.DISLIKE:
            existing_like.delete()  
        else:
            existing_like.update(like_type=LikeType.DISLIKE)  
    else:
        AnswerLike.objects.create(user=profile, answer=answer, like_type=LikeType.DISLIKE)


    like_count = AnswerLike.objects.filter(answer=answer, like_type=LikeType.LIKE).count()
    dislike_count = AnswerLike.objects.filter(answer=answer, like_type=LikeType.DISLIKE).count()
    rating = like_count - dislike_count

    return JsonResponse({
        'status': 'success',
        'rating': rating
    })
@require_POST
@login_required
def set_correct_answer(request, question_id, answer_id):
    question = get_object_or_404(Question, id=question_id)

    if question.author != request.user.profile:
        return JsonResponse({'status': 'error', 'message': 'Only the author can set the correct answer.'}, status=403)

    question.answers.filter(is_correct=True).update(is_correct=False)

    answer = get_object_or_404(Answer, id=answer_id, question=question)
    answer.is_correct = True
    answer.save()

    return JsonResponse({'status': 'success', 'answer_id': answer.id})