#Stores the users score from the quiz.
import json

class Scoreboard:

    def __init__(self):
        self.data = self.get_saves_data()

    def get_saves_data(self):
        try:
            # Try to read the existing scores from the JSON file
            with open('scores.json', 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, create a new one with an empty scores list
            self.data = {
                "scores": []
            }
            with open('scores.json', 'w') as file:
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
    
    def save_score(self, name, score):
        # Append the new score to the scores list
        self.data['scores'].append({
            "name": name,
            "score": score
        })
        # Save the updated scores data back to the JSON file
        with open('scores.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def display_scoreboard(self):
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