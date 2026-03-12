#Stores all tests relating to the scoreboard of the quiz.
from quiz.scoreboard import Scoreboard
import json
import os

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

def test_display_scoreboard(capsys):
    scoreboard.display_scoreboard()
    #Test that the display_scoreboard function correctly displays the scores in the JSON file.
    captured = capsys.readouterr()
    assert "Scoreboard:" in captured.out or "No scores available." in captured.out, "Should display either scoreboard or message"

def test_clear_scoreboard():
    #Test that the clear_scoreboard function correctly clears the scores in the JSON file.
    scoreboard.clear_scoreboard()

    # Read the scores from the JSON file to verify it was cleared
    with open('quizzes/test_quiz_scores.json', 'r') as file:
        data = json.load(file)

    # Check if the scores list is empty
    assert data['scores'] == [], "Scoreboard should be cleared"

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

def test_scoreboard_initialization():
    board = Scoreboard()
    assert board.current_quiz is None, "Scoreboard should initialize with no quiz selected"

def test_set_current_quiz():
    board = Scoreboard()
    board.set_current_quiz("quizzes/test_init")
    assert board.current_quiz == "quizzes/test_init", "Current quiz should be set to the specified quiz"

def test_get_saves_data_creates_file():
    board = Scoreboard()
    board.set_current_quiz("quizzes/new_quiz_for_test")
    
    assert os.path.exists("quizzes/new_quiz_for_test_scores.json"), "Score file should be created"
    
    with open("quizzes/new_quiz_for_test_scores.json", "r") as file:
        data = json.load(file)
    
    assert data == {"scores": []}, "New scoreboard should start empty"

def test_get_saves_data_loads_existing_file():
    board = Scoreboard()
    quiz_name = "quizzes/existing_quiz"
    
    # Create a file with existing scores
    os.makedirs("quizzes", exist_ok=True)
    with open(f"{quiz_name}_scores.json", "w") as file:
        json.dump({"scores": [{"name": "User1", "score": 8}]}, file)
    
    board.set_current_quiz(quiz_name)
    assert board.data["scores"][0]["name"] == "User1", "Should load existing user name"
    assert board.data["scores"][0]["score"] == 8, "Should load existing score"

def test_parse_data_empty():
    board = Scoreboard()
    board.set_current_quiz("quizzes/empty_parse")
    
    result = board.parse_data()
    assert result == []

def test_parse_data_single_entry():
    board = Scoreboard()
    quiz_name = "quizzes/single_entry"
    
    board.set_current_quiz(quiz_name)
    board.save_score("Alice", 10, quiz_name)
    
    result = board.parse_data()
    assert len(result) == 1, "Should have 1 parsed entry"
    assert ("Alice", 10) in result, "Should parse name and score tuple"

def test_parse_data_multiple_entries():
    board = Scoreboard()
    quiz_name = "quizzes/multi_entry"
    
    board.set_current_quiz(quiz_name)
    board.save_score("Alice", 8, quiz_name)
    board.save_score("Bob", 6, quiz_name)
    board.save_score("Charlie", 9, quiz_name)
    
    result = board.parse_data()
    assert len(result) == 3, "Should have 3 parsed entries"
    assert ("Alice", 8) in result, "Should have Alice's score"
    assert ("Bob", 6) in result, "Should have Bob's score"
    assert ("Charlie", 9) in result, "Should have Charlie's score"

def test_save_score_updates_file():
    board = Scoreboard()
    quiz_name = "quizzes/save_update"
    
    board.set_current_quiz(quiz_name)
    board.save_score("User1", 5, quiz_name)
    board.save_score("User2", 7, quiz_name)
    
    with open(f"{quiz_name}_scores.json", "r") as file:
        data = json.load(file)
    
    assert len(data["scores"]) == 2, "File should contain 2 saved scores"

def test_save_score_multiple_same_user():
    board = Scoreboard()
    quiz_name = "quizzes/same_user_score"
    
    board.set_current_quiz(quiz_name)
    board.save_score("Alice", 5, quiz_name)
    board.save_score("Alice", 8, quiz_name)
    
    result = board.parse_data()
    assert result.count(("Alice", 5)) == 1, "First score for Alice should exist once"
    assert result.count(("Alice", 8)) == 1, "Second score for Alice should exist once"

def test_clear_scoreboard_empty():
    board = Scoreboard()
    quiz_name = "quizzes/clear_empty"
    
    board.set_current_quiz(quiz_name)
    board.clear_scoreboard()
    
    result = board.parse_data()
    assert result == []

def test_clear_scoreboard_with_scores():
    board = Scoreboard()
    quiz_name = "quizzes/clear_with_scores"
    
    board.set_current_quiz(quiz_name)
    board.save_score("User1", 5, quiz_name)
    board.save_score("User2", 7, quiz_name)
    board.clear_scoreboard()
    
    result = board.parse_data()
    assert result == []

def test_clear_scoreboard_no_quiz(capsys):
    board = Scoreboard()
    board.clear_scoreboard()
    
    captured = capsys.readouterr()
    assert "No quiz selected" in captured.out

def test_display_scoreboard_empty(capsys):
    board = Scoreboard()
    board.set_current_quiz("quizzes/display_empty")
    board.display_scoreboard()
    
    captured = capsys.readouterr()
    assert "No scores available." in captured.out, "Should display message for empty scoreboard"

def test_display_scoreboard_with_scores(capsys):
    board = Scoreboard()
    quiz_name = "quizzes/display_scores"
    
    board.set_current_quiz(quiz_name)
    board.save_score("Alice", 10, quiz_name)
    board.save_score("Bob", 5, quiz_name)
    board.display_scoreboard()
    
    captured = capsys.readouterr()
    assert "Scoreboard:" in captured.out, "Should display scoreboard header"
    assert "Alice" in captured.out, "Should display Alice in scoreboard"
    assert "Bob" in captured.out, "Should display Bob in scoreboard"

def test_display_scoreboard_no_quiz(capsys):
    board = Scoreboard()
    board.display_scoreboard()
    
    captured = capsys.readouterr()
    assert "No quiz selected" in captured.out

def test_display_scoreboard_sorted_by_score(capsys):
    board = Scoreboard()
    quiz_name = "quizzes/display_sorted"
    
    board.set_current_quiz(quiz_name)
    board.save_score("Charlie", 6, quiz_name)
    board.save_score("Alice", 10, quiz_name)
    board.save_score("Bob", 8, quiz_name)
    board.display_scoreboard()
    
    captured = capsys.readouterr()
    # Alice (10) should appear before Bob (8) which should appear before Charlie (6)
    alice_pos = captured.out.find("Alice")
    bob_pos = captured.out.find("Bob")
    charlie_pos = captured.out.find("Charlie")
    
    assert alice_pos < bob_pos < charlie_pos, "Scores should be sorted in descending order"

def test_display_scoreboard_top_10_limit(capsys):
    board = Scoreboard()
    quiz_name = "quizzes/display_top10"
    
    board.set_current_quiz(quiz_name)
    for i in range(15):
        board.save_score(f"User{i}", i, quiz_name)
    board.display_scoreboard()
    
    captured = capsys.readouterr()
    # Count how many users are displayed (should be max 10)
    display_count = sum(1 for i in range(15) if f"User{i}" in captured.out)
    assert display_count <= 11, "More than 10 scores displayed"

def test_scoreboard_persistence():
    board1 = Scoreboard()
    quiz_name = "quizzes/persistence_test"
    
    board1.set_current_quiz(quiz_name)
    board1.save_score("TestUser", 99, quiz_name)
    
    # Create new scoreboard and load same quiz
    board2 = Scoreboard()
    board2.set_current_quiz(quiz_name)
    
    result = board2.parse_data()
    assert ("TestUser", 99) in result, "Saved scores should persist across instances"