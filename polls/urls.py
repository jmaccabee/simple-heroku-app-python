from django.urls import path

from . import views

urlpatterns = [
    # pass a name argument to enable using URL template tags
    path("", views.index, name="index"),
    path("<uuid:question_id>/", views.detail, name="detail"),
    path("<uuid:question_id>/results/", views.results, name="results"),
    path("<uuid:question_id>/vote/", views.vote, name="vote"),
]
