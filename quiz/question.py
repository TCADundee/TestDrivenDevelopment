#Stores all functions relating to the questions in the quiz.
class Question:

    def __init__(self, text, options, answer): #defines the fields of the question
        self.text = text
        self.options = options
        self.answer = answer

    def check_answer(self, user_answer): #function to check if user answer is true or false
        return user_answer == self.answer