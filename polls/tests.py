"""
The testing system will find tests in any file whose name begins with `test`

Rules of thumb for testing:
- Have a separate test class for each model and view
- Have a separate test method for each set of conditions you want to test
- Test method names should describe their function

We can run these tests automatically from the CLI using:
python manage.py test (<app-name>|<app-name.TestCase>|<app-name.TestCase.method_name>)
Note: passing the flag --pdb will launch the debugger on †est failure

Or we can run them from a shell using:
$ python manage.py shell
>>> from django.test.utils import setup_test_environment
>>> # install a template renderer to examine attributes (like response.context)
>>> # that otherwise wouldn't be available; note this DOESN'T create a test db.
>>> setup_test_environment()
>>> from django.test import Client
>>> use the test client to test endpoints and inspect responses
>>> client = Client()

Note: in database tests, the database is cleared in each method.
Objects created in one method will not carry over to others.
"""
import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    """
    Shortcut function to create new test objects.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """
    Test methods should begin with the prefix: test_
    """

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        # create a Question instance with a pub_date in the future
        future_question = Question(pub_date=time)
        # the return value of was_published_recently() should be false.
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        # use reverse('<app>:<view>') to dynamically lookup the relevant endpoint
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed
        on the index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], ["<Question: Past question.>"]
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed
        on the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past
        questions are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], ["<Question: Past question.>"]
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: Past question 2.>", "<Question: Past question 1.>"],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Question text.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
