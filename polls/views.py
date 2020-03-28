"""
Views should return either an HttpResponse or an Exception.
The render shortcut will return an HttpResponse object by default.
"""
from django.http import HttpResponseRedirect
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


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


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dictionary-like object letting you access data by key name
        # in this case `choice` returns the ID of the selected choice,
        # as a string, since request.POST always returns strings
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    # request.POST will raise a KeyError if a choice wasn't provided in the POST data
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )

    # use the F() function to avoid race conditions where two users might
    # vote before the model has saved the vote. F() references the current
    # field value rather than the value when the object was queried.
    #
    # just be aware that F() assignments persist after save,
    # so be careful saving an object twice after assigning with F()
    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    #
    # HttpResponseRedirect takes 1 parameter (a URL to which the user will be redirected)
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
