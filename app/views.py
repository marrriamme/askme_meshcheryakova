from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Question, Tag, Profile

def index(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': page.object_list,
        'page': page,
        **get_common_context()
    })

def hot(request):
    questions = Question.objects.best_questions() 
    page = paginate(questions, request) 
    return render(request, 'hot.html', {
        'questions': page.object_list,
        'page': page,
        **get_common_context()
    })

def tag(request, tag_name):
    tag_instance = get_object_or_404(Tag, name=tag_name)
    questions = tag_instance.questions.all()
    page = paginate(questions, request)
    return render(request, 'bender.html', {
        'tag_name': tag_name,
        'questions': page.object_list,
        'page': page,
        **get_common_context()
    })

def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers_page = paginate(question.answers.all(), request)
    return render(request, 'question.html', {
        'question': question,
        'answers': answers_page.object_list,
        'answers_count': question.answers.count(),
        'page': answers_page,
        **get_common_context()
    })

def ask(request):
    return render(request, 'ask.html', get_common_context())

def login(request):
    return render(request, 'login.html', get_common_context())

def settings(request):
    return render(request, 'settings.html', get_common_context())

def signup(request):
    return render(request, 'signup.html', get_common_context())

def get_common_context():
    return {
        'tags': Tag.objects.all()[:20],
        'members': Profile.objects.all()[:20]  
    }

def paginate(objects_list, request, per_page=30):
    page_number = request.GET.get('page', 1)
    per_page_param = request.GET.get('per_page', per_page)

    try:
        per_page = int(per_page_param)
        if per_page <= 0:
            per_page = 10  
    except ValueError:
        per_page = 30  

    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
