#Stores all tests relating to the scoreboard of the quiz.
from quiz.scoreboard import Scoreboard
import json

scoreboard = Scoreboard()

def test_save_score():
    #Test that the save_score function correctly saves a score to the JSON file.
    name = "Test User"
    score = 5
    scoreboard.save_score(name, score)

    # Read the scores from the JSON file to verify the new score was saved
    with open('scores.json', 'r') as file:
        data = json.load(file)

    # Check if the new score is in the data
    assert any(entry['name'] == name and entry['score'] == score for entry in data['scores'])

def test_display_scoreboard():
    scoreboard.display_scoreboard()
    #Test that the display_scoreboard function correctly displays the scores in the JSON file.

test_display_scoreboard()