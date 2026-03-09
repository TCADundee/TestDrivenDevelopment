#Stores all tests relating to a quiz.
from quiz.quiz import Quiz
from quiz.question import Question


def test_quiz_stores_questions():

    q1 = Question("2+2?", ["3", "4"], "4")

    quiz = Quiz([q1])

    assert len(quiz.questions) == 1