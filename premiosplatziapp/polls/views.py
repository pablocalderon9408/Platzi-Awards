from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from jinja2 import TemplateError
from polls.models import Question
# Create your views here.

def index(request):
    latest_question_list = Question.objects.all()
    return render(request, template_name="polls/index.html", context={
        "latest_question_list": latest_question_list
    })

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, template_name="polls/detail.html", context={
        "question":question
    })

def results(request, question_id):
    return HttpResponse(f"Estás viendo los resultados de la pregunta número {question_id}")

def vote(request, question_id):
    return HttpResponse(f"Estás votando a la pregunta número {question_id}")

