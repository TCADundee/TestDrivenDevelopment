#Stores the users score from the quiz.
import json

class Scoreboard:

    def __init__(self):
        self.current_quiz = None

    def set_current_quiz(self, quiz_name):
        self.current_quiz = quiz_name
        self.get_saves_data() #Loads the scores for the selected quiz.

    def get_saves_data(self):
        if self.current_quiz is None:
            return None

        try:
            # Try to read the existing scores from the JSON file
            with open(f'{self.current_quiz}_scores.json', 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("Scoreboard file not found. Creating a new one...")
            # If the file does not exist, create a new one with an empty scores list
            self.data = {
                "scores": []
            }
            with open(f'{self.current_quiz}_scores.json', 'w') as file:
                json.dump(self.data, file)

        return self.data
    
    def parse_data(self):
        # Parse the scores data and return a list of tuples (name, score)
        scores = []
        for entry in self.data['scores']:
            name = entry['name']
            score = entry['score']
            scores.append((name, score))
        return scores
    
    def save_score(self, name, score, current_quiz):
        if self.current_quiz is None:
            self.current_quiz = current_quiz

        # Append the new score to the scores list
        self.data['scores'].append({
            "name": name,
            "score": score
        })
        # Save the updated scores data back to the JSON file
        with open(f'{current_quiz}_scores.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def clear_scoreboard(self):
        if self.current_quiz is None:
            print("No quiz selected. Cannot clear scoreboard.")
            return
        # Clear the scores list and save the empty data back to the JSON file
        self.data['scores'] = []
        with open(f'{self.current_quiz}_scores.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def display_scoreboard(self):
        print(self.current_quiz)
        if self.current_quiz is None:
            print("No quiz selected. Cannot display scoreboard.")
            return

        if not self.data or 'scores' not in self.data or self.data['scores'] == []:
            print("\nNo scores available.")
            return

        # Parse the scores data
        scores = self.parse_data()

        # Sort the scores in descending order
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        # Display the top 10 scores
        print("\nScoreboard:")
        for i, (name, score) in enumerate(sorted_scores[:10]):
            print(f"{i + 1}. {name}: {score}")