from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Question
# Create your views here.

def index(request):
    latest_question_list = Question.objects.all()
    return render(request, template_name="polls/index.html", context={
        "latest_question_list": latest_question_list
    })

def detail(request, question_id):
    return HttpResponse(f"Estás viendo la pregunta número {question_id}")


def results(request, question_id):
    return HttpResponse(f"Estás viendo los resultados de la pregunta número {question_id}")

def vote(request, question_id):
    return HttpResponse(f"Estás votando a la pregunta número {question_id}")

