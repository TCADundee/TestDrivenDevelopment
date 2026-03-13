#Runs a quiz game, asking the user questions and keeping track of their score.

class Quiz:

    def __init__(self, questions):
        self.questions = questions
        self.score = 0 #keeps track of score

    def run(self): #function that runs the quiz

        for question in self.questions: #loops for all questions

            user_answer = question.ask_question() #asks the question and gets the user's answer              
            
            if question.check_answer(user_answer): #checks if the answer is correct by calling a function that returns true or false
                print("Correct!")
                self.score += 1
            else:
                print("Incorrect!")

        print("\nQuiz finished!")
        print("Your score:", self.score, "/", len(self.questions)) #prints score 
        return self.score