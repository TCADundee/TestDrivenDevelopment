# This file will contain the automated tests for the quiz application
from quiz.scoreboard import Scoreboard

def test_scoreboard():
    print("\n\n\n--- Testing Scoreboard ---\n")

    scoreboard = Scoreboard()

    if scoreboard.data and 'scores' in scoreboard.data and scoreboard.data['scores'] != []:
        # Clear the scoreboard before testing
        print("Clearing scoreboard before testing...")
        scoreboard.clear_scoreboard()
        assert scoreboard.data == {"scores": []}, "Scoreboard should be empty after clearing"   
    
    # Test saving a score to scoreboard
    scoreboard.save_score("Alice", 5)
    # Test saving another score to scoreboard
    scoreboard.save_score("Bob", 3)

    # Test displaying the scoreboard
    scoreboard.display_scoreboard()
    # Test that the scores are saved correctly
    assert scoreboard.data["scores"][0]["name"] == "Alice", "First score name should be Alice"
    assert scoreboard.data["scores"][0]["score"] == 5, "First score should be 5"
    assert scoreboard.data["scores"][1]["name"] == "Bob", "Second score name should be Bob"
    assert scoreboard.data["scores"][1]["score"] == 3, "Second score should be 3"

    print("\n--- Scoreboard tests completed ---\n")
    return True

if __name__ == "__main__":
    result =  test_scoreboard()
    if result:
        print("All scoreboard tests passed!")