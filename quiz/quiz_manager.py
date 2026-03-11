#Stores functions to manage the quiz, including loading a quiz ,as well as modifying, adding and removing questions.
import os
import json
from quiz.question import Question
from quiz.quiz import Quiz


class QuizManager:

    #Loads a quiz from a JSON file and returns a Quiz object.
    def load_quiz(self, filename):

        with open(filename, "r") as file:
            data = json.load(file)

        questions = []

        for item in data:
            question = Question(
                item["text"],
                item["options"],
                item["answer"]
            )
            questions.append(question)

        return Quiz(questions)

    #Loads a menu with all modification options for the quiz, including listing questions, adding a question, removing a question and updating a question.
    def modify_quiz(self, filename):
        while True:
            print("\nQuiz Modification Menu:")
            print("1. List Questions")
            print("2. Add Question")
            print("3. Remove Question")
            print("4. Update Question")
            print("5. Back to Main Menu")

            choice = input("Choose an option: ")

            match choice:
                case "1":#Lists all questions in the current quiz.
                    self.list_questions(filename)


                case "2":#Adds a new question to the quiz.

                    question = self.validate_question()#Receives validated question.
                    self.add_question(filename, question)


                case "3":#Removes a question from the quiz.
                    self.list_questions(filename)

                    try:
                        number = int(input("Enter question number to remove: "))
                        self.remove_question(filename, number)
                    except ValueError:
                        print("Invalid input. Please enter a number.")


                case "4": #Lists all questions and allows user to select a question to update.
                    self.list_questions(filename)

                    try:#Validates input for question number to update.
                        number = int(input("Enter question number to update: "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue    

                    #Load quiz data
                    with open(filename, "r") as file:
                        data = json.load(file)

                    index = number - 1

                    #Validate question that is to be modified exists.
                    if index < 0 or index >= len(data):
                        print("Invalid question number.")
                        continue
                    
                    #Shows question selected for modification.
                    print("\nEditing Question:")
                    print("Text:", data[index]["text"])
                    print("Options:", data[index]["options"])
                    print("Answer:", data[index]["answer"])

                    question = self.validate_question() #Receives validated question.
                    self.update_question(filename, number, question)


                case "5": #Returns to the main menu.
                    break
                case _:
                    print("Invalid option. Please try again.")

                    
    #Adds a new question to the quiz by appending it into the JSON file.
    def add_question(self, filename, question):

        with open(filename, "r") as file:
            data = json.load(file)

        data.append({
            "text": question.text,
            "options": question.options,
            "answer": question.answer
        })

        with open(filename, "w") as file:
            json.dump(data, file, indent=2)


    #Lists all questions in json file.
    def list_questions(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        for i, item in enumerate(data, 1):
            print(f"\nQuestion {i}")
            print("Text:", item["text"])
            print("Options:", item["options"])
            print("Answer:", item["answer"])
 

    #Deletes a question.
    def remove_question(self, filename, question_number):
        with open(filename, "r") as file:
            data = json.load(file)

        index = question_number - 1
        if index < 0 or index >= len(data):
            print("Invalid question number")
            return

        del data[index]
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)

        

    #Updates an already exisiting question.
    def update_question(self, filename, question_number, new_question):
        with open(filename, "r") as file:
            data = json.load(file)

        index = question_number - 1

        data[index] = {
            "text": new_question.text,
            "options": new_question.options,
            "answer": new_question.answer
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=2)


    #Lists all quizzes in the quizzes folder.
    def list_quizzes(self, folder="quizzes"):
        if not os.path.exists(folder):
            os.mkdir(folder)

        quiz_files = []

        for file in os.listdir(folder):
            if file.endswith(".json"):
                quiz_files.append(file)

        return quiz_files


    #Allows you to create a new quiz.
    def create_quiz(self, filename, folder="quizzes"):
        if not os.path.exists(folder):
            os.mkdir(folder)

        full_path = os.path.join(folder, filename)

        if not full_path.endswith(".json"):
            full_path += ".json"

        if os.path.exists(full_path):
            print("Quiz already exists.")
            return

        with open(full_path, "w") as file:
            json.dump([], file, indent=2)

        print("Quiz created:", full_path)

    #Question Verification, added to avoid reusing same code for validating update and add question functions.
    def validate_question(self):
        while True:#Validates question text, looping until a non-empty question is entered.
            text = input("Enter question text: ").strip()
            if text:
                break
            print("Question text cannot be empty. Please try again.")

        while True:#Validates options, looping until at least 2 options are entered.
            options = input("Enter options separated by commas: ").split(",")
            options = [option.strip() for option in options if option.strip()] #removes empty options
            if len(options) >= 2:
                break
            print("Please enter at least 2 options.")

        while True:#Validates answer, looping until a non-empty answer is entered that is also one of the options.
            answer = input("Enter the correct answer: ").strip()
            if answer and answer in options:
                break
            print("Answer must be one of the options and cannot be empty. Please try again.")

        return Question(text, options, answer)