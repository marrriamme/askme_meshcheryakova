from django.shortcuts import render
from django.http import HttpResponse
import copy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random

AVAILABLE_TAGS = [f'tag name {i}' for i in range(20)]
AVAILABLE_ANSWERS = [f'answer id {i}' for i in range(20)]

QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'This text for question # {i}',
        'answers': [{'id': j, 'text': f'Answer text for question {i}, answer {j}'} for j in range(random.randint(0, 20))], 
        'tags': random.sample(AVAILABLE_TAGS, 3)  
    } for i in range(60)
]


TAGS = [
    {
        'name': f'tag name {i}',
    } for i in range(20)
]

MEMBERS = [
    {
        'name': f'member name {i}',
    } for i in range(10)
]


def index(request):
    page = paginate(QUESTIONS, request)
    questions_with_counts = [
        {**question, 'answers_count': len(question['answers'])} for question in page.object_list
    ]
    return render(
        request, 'index.html', 
        {'questions': questions_with_counts, 'tags': TAGS, 'page': page, 'members': MEMBERS}
    )

def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    page = paginate(hot_questions, request)
    questions_with_counts = [
        {**question, 'answers_count': len(question['answers'])} for question in page.object_list
    ]
    return render(
        request, 'hot.html',
        {'questions': questions_with_counts, 'tags': TAGS, 'page': page, 'members': MEMBERS}
    )

def tag(request, tag_name):
    filtered_questions = [q for q in QUESTIONS if tag_name in q['tags']]
    page = paginate(filtered_questions, request)
    questions_with_counts = [
        {**question, 'answers_count': len(question['answers'])} for question in page.object_list
    ]
    return render(request, 'bender.html', {
        'tag_name': tag_name,
        'questions': questions_with_counts,
        'tags': TAGS,
        'page': page,
        'members': MEMBERS
    })





def question(request, question_id):
    question = QUESTIONS[question_id]
    answers_page = paginate(question['answers'], request)
    
    answers_count = len(question['answers'])
    
    return render(
        request, 'question.html',
        {
            'question': question,
            'answers': answers_page.object_list,
            'answers_count': answers_count,  
            'tags': TAGS,
            'page': answers_page,
            'members': MEMBERS
        }
    )


def ask(request):
    return render(
        request, 'ask.html',
        {'tags': TAGS, 'members':  MEMBERS}
    )

def login(request):
    return render(
        request, 'login.html',
        {'tags': TAGS, 'members':  MEMBERS}
    )

def settings(request):
    return render(
        request, 'settings.html',
        {'tags': TAGS, 'members':  MEMBERS}
    )

def signup(request):
    return render(
        request, 'signup.html',
        {'tags': TAGS, 'members':  MEMBERS}
    )


def paginate(objects_list, request):
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 20)

    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10  

    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


