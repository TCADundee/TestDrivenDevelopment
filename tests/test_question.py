#Stores all tests relating to the questions in the quiz.
from quiz.question import Question

def test_question_correct_answer():
    question = Question("What is the largest desert in the world?",
                         ["Sahara", "Gobi", "Kalahari", "Antarctica"],
                         "Antarctica")
    
    assert question.check_answer("Antarctica")


def test_question_incorrect_answer():
    question = Question("What is the largest desert in the world?",
                         ["Sahara", "Gobi", "Kalahari", "Antarctica"],
                         "Antarctica")

    assert not question.check_answer("Sahara")