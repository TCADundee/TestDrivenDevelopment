#Stores all tests related to the core functionality of the quiz management system.
from quiz.quiz_manager import QuizManager


def test_load_quiz():

    manager = QuizManager()

    quiz = manager.load_quiz("quiz_data.json")

    assert len(quiz.questions) > 0

def test_load_quiz_invalid_file():

    manager = QuizManager()

    try:
        quiz = manager.load_quiz("non_existent_file.json")
        assert False, "Expected an exception for a non-existent file"
    except FileNotFoundError:
        pass  # Expected

#def test_add_question():

#def test_remove_question():

#def test_modify_question():