import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question, Choice

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quién es el mejor CD de platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        print("Hice el test # 1")

    def test_was_published_recently_with_now_question(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now()
        now_question = Question(question_text="Quién es el mejor CD de platzi?", pub_date=time)
        self.assertIs(now_question.was_published_recently(), True)
        print("Hice el test # 2")

    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(question_text="Quién es el mejor CD de platzi?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
        print("Hice el test # 3")


def create_questions(question_text, days):
    """Create a question with the given question_text, and publish the given
    number of days offset to now."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choices(question, choice_text):
    """Create a choice with the given choice_text associated to the given question."""
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionResultViewTest(TestCase):
    def test_question_without_choices_are_not_rendered(self):
        question = create_questions("Base question", days=-10)
        choices = question.choice_set.all()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"][0].choice_set.all(), [])
        print("Hice el test # 4")

    def test_question_always_have_choices(self):
        question = create_questions("Base question", days=-10)
        choice = create_choices (question, "Base choice" )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        print("Hice el test # 5")


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exists, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        print("Hice el test # 6")

    def test_no_future_questions_rendered(self):
        """If a question's pub_date is in the future, it can not be rendered."""
        create_questions("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        print("Hice el test # 7")

    def test_past_questions(self):
        """If a question's pub_date is in the past, it must be rendered."""
        question = create_questions("Past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        print("Hice el test # 8")

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        past_question = create_questions("Past question", days=-30)
        future_question = create_questions("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])
        print("Hice el test # 9")

    def test_two_past_questions(self):
        past_question_1 = create_questions("Past question #1", days=-20)
        past_question_2 = create_questions("Past question #2", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question_1, past_question_2])
        print("Hice el test # 10")


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future return a 404 error"""
        future_question = create_questions("Future question", days=30)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        print("Hice el test # 11")

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question text"""
        past_question = create_questions("Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        print("Hice el test # 12")
