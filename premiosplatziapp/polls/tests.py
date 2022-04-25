import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question

class QuestionModelTests(TestCase):
    """"""

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quién es el mejor CD de platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_now_question(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now()
        now_question = Question(question_text="Quién es el mejor CD de platzi?", pub_date=time)
        self.assertIs(now_question.was_published_recently(), True)

    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(question_text="Quién es el mejor CD de platzi?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)


def create_questions(question_text, days):
    """Create a question with the given question_text, and publish the given
    number of days offset to now."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exists, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def no_future_questions_rendered(self):
        """If a question's pub_date is in the future, it can not be rendered."""
        create_questions("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def past_questions(self):
        """If a question's pub_date is in the future, it can not be rendered."""
        question = create_questions("Future question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
