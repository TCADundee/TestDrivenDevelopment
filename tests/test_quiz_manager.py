#Stores all tests related to the core functionality of the quiz management system.
from quiz.quiz_manager import QuizManager
from quiz.question import Question
import json, os, pytest, atexit

def test_load_quiz():

    manager = QuizManager()

    quiz = manager.load_quiz("quizzes/quiz_data.json")

    assert len(quiz.questions) > 0, "Quiz should load at least one question"

def test_load_quiz_invalid_file():

    manager = QuizManager()

    with pytest.raises(FileNotFoundError):
        manager.load_quiz("quizzes/non_existent_file.json")

def test_create_quiz():
    manager = QuizManager()
    
    manager.create_quiz("test_quiz.json")
    
    assert os.path.exists("quizzes/test_quiz.json"), "Quiz file should be created"
    
    with open("quizzes/test_quiz.json", "r") as file:
        data = json.load(file)

    assert data == [], "Newly created quiz should be empty"

def test_create_quiz_without_extension():
    manager = QuizManager()
    
    manager.create_quiz("test_quiz_without_extension")
    
    import os
    assert os.path.exists("quizzes/test_quiz_without_extension.json"), "Should add .json extension automatically"
    
    with open("quizzes/test_quiz_without_extension.json", "r") as file:
        data = json.load(file)
    
    assert data == [], "Quiz should be empty after creation"

def test_create_quiz_already_exists(capsys):
    manager = QuizManager()
    
    manager.create_quiz("test_existing_quiz.json")
    manager.create_quiz("test_existing_quiz.json")
    
    captured = capsys.readouterr()
    assert "Quiz already exists." in captured.out, "Should display message when quiz already exists"

def test_add_question():
    manager = QuizManager()

    question = Question("What is the capital of France?", ["Paris", "London", "Berlin"], "Paris")
    manager.add_question("quizzes/test_quiz.json", question)

    assert question.text == "What is the capital of France?", "Question text should match"
    assert question.options == ["Paris", "London", "Berlin"], "Question options should match"
    assert question.answer == "Paris", "Question answer should match"


def test_modify_question():
    manager = QuizManager()

    manager.update_question("quizzes/test_quiz.json", 1, Question("What is the capital of Germany?", ["Paris", "London", "Berlin"], "Berlin"))

    with open("quizzes/test_quiz.json", "r") as file:
        data = json.load(file)

    assert data[0]["text"] == "What is the capital of Germany?", "Question text should be updated"
    assert data[0]["options"] == ["Paris", "London", "Berlin"], "Question options should be updated"
    assert data[0]["answer"] == "Berlin", "Question answer should be updated"

def test_remove_question():
    manager = QuizManager()

    manager.remove_question("quizzes/test_quiz.json", 1)

    with open("quizzes/test_quiz.json", "r") as file:
        data = json.load(file)

    assert len(data) == 0, "All questions should be removed"

def test_list_questions(capsys):
    manager = QuizManager()
    
    manager.add_question("quizzes/test_quiz.json", Question("What is 2+2?", ["3", "4", "5"], "4"))
    manager.add_question("quizzes/test_quiz.json", Question("What is the capital of France?", ["Paris", "London", "Berlin"], "Paris"))
    
    manager.list_questions("quizzes/test_quiz.json")
    
    captured = capsys.readouterr()
    assert "Question 1" in captured.out, "Should display first question"
    assert "Question 2" in captured.out, "Should display second question"
    assert "What is 2+2?" in captured.out, "Should display first question text"
    assert "What is the capital of France?" in captured.out, "Should display second question text"

def test_list_quizzes():
    manager = QuizManager()
    
    manager.create_quiz("test_quiz_1.json")
    manager.create_quiz("test_quiz_2.json")
    
    quizzes = manager.list_quizzes("quizzes")
    
    assert "test_quiz_1.json" in quizzes, "Should list created quiz 1"
    assert "test_quiz_2.json" in quizzes, "Should list created quiz 2"

def test_list_quizzes_filters_score_files():
    manager = QuizManager()
    
    manager.create_quiz("test_quiz_filter.json")
    
    quizzes = manager.list_quizzes("quizzes")
    
    # Ensure score files are not included
    for quiz in quizzes:
        assert not quiz.endswith("_scores.json"), "Score files should not be included in quiz list"

def test_remove_question_invalid_number():
    manager = QuizManager()
    clear_test_file()

    question = Question("Test?", ["A", "B"], "A")
    manager.add_question("quizzes/test_quiz.json", question)
    
    manager.remove_question("quizzes/test_quiz.json", 999)
    
    with open("quizzes/test_quiz.json", "r") as file:
        data = json.load(file)
    
    assert len(data) == 1, "Invalid remove should not delete the question"

def test_update_question_invalid_number():
    manager = QuizManager()
    clear_test_file()

    question1 = Question("Original?", ["A", "B"], "A")
    manager.add_question("quizzes/test_quiz.json", question1)
    
    question2 = Question("Updated?", ["X", "Y"], "X")
    manager.update_question("quizzes/test_quiz.json", 999, question2)
    
    with open("quizzes/test_quiz.json", "r") as file:
        data = json.load(file)
    
    # Question should remain unchanged
    assert data[0]["text"] == "Original?", "Invalid update should not modify the question"

def clear_test_file():
    with open("quizzes/test_quiz.json", "w") as file:
        json.dump([], file)

#Deletes test files after all tests finish running.
def cleanup_test_files():

    folder = "quizzes"

    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):

        #Remove temporary quiz files
        if file.startswith("test_") or file.endswith("_scores.json"):
            try:
                os.remove(os.path.join(folder, file))
            except FileNotFoundError:
                pass


#Register cleanup when pytest finishes
atexit.register(cleanup_test_files)