#Stores all tests relating to a quiz.
from quiz.quiz import Quiz
from quiz.question import Question
from unittest.mock import patch
import io


def test_quiz_stores_questions():

    q1 = Question("2+2?", ["3", "4"], "4")

    quiz = Quiz([q1])

    assert len(quiz.questions) == 1, "Quiz should store exactly one question"

def test_quiz_initialization():
    q1 = Question("Q1?", ["A", "B"], "A")
    q2 = Question("Q2?", ["X", "Y"], "X")
    
    quiz = Quiz([q1, q2])
    
    assert len(quiz.questions) == 2, "Quiz should store 2 questions"
    assert quiz.score == 0, "Quiz score should initialize to 0"

def test_quiz_score_initialization():
    q1 = Question("2+2?", ["3", "4"], "4")
    
    quiz = Quiz([q1])
    
    assert quiz.score == 0, "Quiz score should initialize to 0"

def test_quiz_stores_multiple_questions():
    questions = [
        Question("Q1?", ["A", "B"], "A"),
        Question("Q2?", ["X", "Y"], "X"),
        Question("Q3?", ["1", "2"], "1")
    ]
    
    quiz = Quiz(questions)
    
    assert len(quiz.questions) == 3, "Quiz should store 3 questions"
    assert quiz.questions[0].text == "Q1?", "First question text should be Q1?"
    assert quiz.questions[1].text == "Q2?", "Second question text should be Q2?"
    assert quiz.questions[2].text == "Q3?", "Third question text should be Q3?"

def test_quiz_with_no_questions():
    quiz = Quiz([])
    
    assert len(quiz.questions) == 0, "Quiz with empty list should have 0 questions"
    assert quiz.score == 0, "Empty quiz score should be 0"

def test_quiz_run_all_correct_answers(capsys):
    questions = [
        Question("2+2?", ["3", "4"], "4"),
        Question("5+5?", ["10", "11"], "10")
    ]
    
    quiz = Quiz(questions)
    
    with patch('builtins.input', side_effect=['2', '1']):
        score = quiz.run()
    
    captured = capsys.readouterr()
    assert "Correct!" in captured.out, "Output should display 'Correct!' for correct answers"
    assert score == 2, "Score should be 2 for 2 correct answers"
    assert quiz.score == 2, "Quiz score should be updated to 2"

def test_quiz_run_all_incorrect_answers(capsys):
    questions = [
        Question("2+2?", ["3", "4"], "4"),
        Question("5+5?", ["10", "11"], "10")
    ]
    
    quiz = Quiz(questions)
    
    with patch('builtins.input', side_effect=['1', '2']):
        score = quiz.run()
    
    captured = capsys.readouterr()
    assert "Incorrect!" in captured.out, "Output should display 'Incorrect!' for wrong answers"
    assert score == 0, "Score should be 0 for 0 correct answers"
    assert quiz.score == 0, "Quiz score should remain 0"


def test_quiz_run_single_question(capsys):
    questions = [Question("What is 1+1?", ["1", "2"], "2")]
    
    quiz = Quiz(questions)
    
    with patch('builtins.input', return_value='2'):
        score = quiz.run()
    
    assert score == 1, "Score should be 1 for 1 correct answer"
    assert quiz.score == 1, "Quiz score should be 1"

def test_quiz_run_displays_questions(capsys):
    questions = [Question("What is the capital of France?", ["Paris", "London"], "Paris")]
    
    quiz = Quiz(questions)
    
    with patch('builtins.input', return_value='1'):
        quiz.run()
    
    captured = capsys.readouterr()
    assert "What is the capital of France?" in captured.out, "Question text should be displayed"
    assert "Paris" in captured.out, "Answer option Paris should be displayed"
    assert "London" in captured.out, "Answer option London should be displayed"
    assert "1. Paris" in captured.out, "Options should be numbered correctly"
    assert "2. London" in captured.out, "Options should be numbered correctly"

def test_quiz_run_displays_final_score(capsys):
    questions = [
        Question("Q1?", ["A", "B"], "A"),
        Question("Q2?", ["X", "Y"], "X")
    ]
    
    quiz = Quiz(questions)
    
    with patch('builtins.input', side_effect=['1', '1']):
        quiz.run()
    
    captured = capsys.readouterr()
    assert "Your score:" in captured.out, "Final score message should be displayed"
    assert "2 /" in captured.out, "Score summary should show 2 correct answers"

def test_quiz_run_returns_score():
    questions = [Question("2+2?", ["3", "4"], "4")]
    
    quiz = Quiz(questions)
    
    with patch('builtins.input', return_value='2'):
        returned_score = quiz.run()
    
    assert returned_score == 1, "run() should return the final score"
    assert returned_score == quiz.score, "Returned score should match quiz.score"

def test_quiz_questions_are_independent():
    q1 = Question("Q1?", ["A", "B"], "A")
    q2 = Question("Q2?", ["X", "Y"], "X")
    
    quiz1 = Quiz([q1])
    quiz2 = Quiz([q2])
    
    assert quiz1.questions[0].text == "Q1?", "Quiz 1 should have its own question"
    assert quiz2.questions[0].text == "Q2?", "Quiz 2 should have its own question"
    assert quiz1.score == quiz2.score == 0, "Both quizzes should start with score 0"

def test_quiz_order_of_questions_preserved():
    questions = [
        Question("First?", ["A", "B"], "A"),
        Question("Second?", ["X", "Y"], "X"),
        Question("Third?", ["1", "2"], "1")
    ]
    
    quiz = Quiz(questions)
    
    assert quiz.questions[0].text == "First?", "First question should be at index 0"
    assert quiz.questions[1].text == "Second?", "Second question should be at index 1"
    assert quiz.questions[2].text == "Third?", "Third question should be at index 2"