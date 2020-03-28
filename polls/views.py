"""
Views should return either an HttpResponse or an Exception
"""
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # render takes the request object as its first argument,
    # a template name as it's second argument,
    # and a dictionary as its optional third argument (context)
    # it returns an HttpResponse object of the template rendered with the context
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    # get_object_or_404 takes a Django model as its first argument and an arbitrary number of
    # keyword arguments, which it passes to the get() function of the model's manager
    # and raises Http404 if the object doesn't exist.
    #
    # there's also a get_list_or_404() function, except using filter() instead of get().
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question {}."
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))
