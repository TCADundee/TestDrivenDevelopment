## Quiz Program

A simple quiz application written in Python.
The program allows users to play quizzes, create new quizzes, modify existing quizzes, and track scores.

The project was developed using Test-Driven Development (TDD) with automated tests written using pytest.

Made by Callum Laidlaw, Ryan Dowey and Thomas Anderson.

## Features

Load quizzes from JSON files.

Play quizzes.

Add, update, and remove quiz questions.

Create new quizzes.

View and manage quizzes stored in a folder.

Score tracking via a scoreboard system.

Automated testing using pytest framework.

## Structure

- `quiz/`
  - `__init__.py` 
  - `quiz.py` (Main quiz Functionality)
  - `question.py`(Question Functionality)
  - `quiz_manager.py` (Quiz modification Functionality)
  - `scoreboard.py` (User score Tracking and Storing)
- `tests/`
  - `test_question.py` ( tests relating to the question file)
  - `test_quiz_manager.py`( tests relating to the quiz manager)
  - `test_quiz.py`(tests relating to the game side of the quiz)
  - `test_scoreboard.py`(tests relating to the scoreboard)
  - `automated_tests.py`(Used before pytest implementation)

