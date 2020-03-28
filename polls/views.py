"""
Views should return either an HttpResponse or an Exception.
The render shortcut will return an HttpResponse object by default.

Generic views abstract common patterns:
1) Get data from the db according to a URL parameter
2) Load a template
3) return the rendered template

Generic views also enable automatic context generation
based on the name of the model you pass.

For a DetailView, `<model_name>` is automatically included in
our templates' context.

For a ListView, `<model_name>_list` is included in our context.
"""
from django.http import HttpResponseRedirect
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    A ListView represents a page with a list of objects.

    Requires a template and a context to populate
    the template with.

    self.object_list contains the list of objects that the view is operating on.
    """

    # if our HTML was <model_name>_list.html (i.e., question_list.html),
    # we could skip this next line altogether
    template_name = "polls/index.html"
    # since our previous view defined our object list context as
    # "latest_question_list", we must explicitly pass a context_object_name.
    # had we used "question_list" instead, this wouldn't be necessary.
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions
        """
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    A DetailView requires a model and a template to display.

    self.object contains the object the view is operating on.
    """

    model = Question
    # if our HTML was <model_name>_detail.html (i.e., question_detail.html),
    # we could skip this next line altogether by default
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """
    A DetailView requires a model and a template to display.

    self.object contains the object the view is operating on.
    """

    model = Question
    # if our HTML was <model_name>_detail.html (i.e., question_detail.html),
    # we could skip this next line altogether by default
    template_name = "polls/results.html"


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
