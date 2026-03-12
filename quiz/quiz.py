#Runs a quiz game, asking the user questions and keeping track of their score.

class Quiz:

    def __init__(self, questions):
        self.questions = questions
        self.score = 0

    def run(self):

        for question in self.questions:

            print("\n" + question.text)

            for i, option in enumerate(question.options, 1):
                print(f"{i}. {option}")

            #Checks the number input by the user and converts it to the corresponding option,
            #then checks if the answer is correct and updates the score accordingly.
            while True:
                try:
                    answer_index = int(input("Choose an option: ")) - 1
                    if 0 <= answer_index < len(question.options):
                        user_answer = question.options[answer_index]
                        break
                    else:
                        print("Please enter a valid option number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
            
            
            if question.check_answer(user_answer):
                print("Correct!")
                self.score += 1
            else:
                print("Incorrect!")

        print("\nQuiz finished!")
        print("Your score:", self.score, "/", len(self.questions))
        return self.score