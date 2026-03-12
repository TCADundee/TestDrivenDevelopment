#Stores all tests relating to the scoreboard of the quiz.
from quiz.scoreboard import Scoreboard
import json

scoreboard = Scoreboard()
scoreboard.set_current_quiz("quizzes/test_quiz") #Sets the current quiz to test_quiz, allowing the tests to load and save scores for that quiz.

def test_save_score():
    #Test that the save_score function correctly saves a score to the JSON file.
    name = "Test User"
    score = 5
    scoreboard.save_score(name, score, "quizzes/test_quiz")

    # Read the scores from the JSON file to verify the new score was saved
    with open('quizzes/test_quiz_scores.json', 'r') as file:
        data = json.load(file)

    # Check if the new score is in the data
    assert any(entry['name'] == name and entry['score'] == score for entry in data['scores'])

def test_display_scoreboard():
    scoreboard.display_scoreboard()
    #Test that the display_scoreboard function correctly displays the scores in the JSON file.

def test_clear_scoreboard():
    #Test that the clear_scoreboard function correctly clears the scores in the JSON file.
    scoreboard.clear_scoreboard()

    # Read the scores from the JSON file to verify it was cleared
    with open('quizzes/test_quiz_scores.json', 'r') as file:
        data = json.load(file)

    # Check if the scores list is empty
    assert data['scores'] == []

def test_multiple_scoreboards():
    #Test that multiple scoreboards can be created and accessed correctly.
    scoreboard.set_current_quiz("quizzes/test_quiz_2") #Sets the current quiz to test_quiz_2, allowing the tests to load and save scores for that quiz.

    name = "Test User 2"
    score = 7
    scoreboard.save_score(name, score, "quizzes/test_quiz_2")

    # Read the scores from the JSON file to verify the new score was saved
    with open('quizzes/test_quiz_2_scores.json', 'r') as file:
        data = json.load(file)

    # Check if the new score is in the data
    assert any(entry['name'] == name and entry['score'] == score for entry in data['scores'])