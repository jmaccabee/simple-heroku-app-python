from django.urls import path

from . import views


# enable URL namespacing in URL template tags by setting an app_name.
app_name = "polls"
urlpatterns = [
    # pass a name argument to enable using URL template tags
    path("", views.IndexView.as_view(), name="index"),
    # for generic views (list DetailView), the URL parameter is expected to be named pk
    path("<uuid:pk>/", views.DetailView.as_view(), name="detail"),
    path("<uuid:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<uuid:question_id>/vote/", views.vote, name="vote"),
]
