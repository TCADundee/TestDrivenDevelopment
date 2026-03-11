#Main file, allows users to select between playing a quiz, switching quiz, testing or exiting the program.
import os
from quiz.quiz_manager import QuizManager
from quiz.scoreboard import Scoreboard
from quiz.question import Question

manager = QuizManager()
scoreboard = Scoreboard()
current_quiz = None
while True:

    print("\n--- Quiz Menu ---")
    print("1. List Quiz")
    print("2. Select Quiz")
    print("3. Create Quiz")
    print("4. Play Quiz")
    print("5. View Questions")
    print("6. Add Question")
    print("7. Remove Question")
    print("8. Update Question")
    print("9. View Scoreboard")
    print("10. Exit")

    choice = input("Choose an option: ")

    match choice:
        case "1": #case for list quizzes
            quizzes = manager.list_quizzes() 
            if not quizzes: #checks if there are quizzes 
                print("No quizzes available.")
            else:
                print("\nAvailable quizzes:") #prints quizzes
                for i, quiz_file in enumerate(quizzes, 1):
                    print(f"{i}. {quiz_file}")

        case "2": #case for select quiz
            quizzes = manager.list_quizzes()
            if not quizzes: #chekcs if quizzes
                print("No quizzes available.")
            else:
                print("\nAvailable quizzes:")
                for i, quiz_file in enumerate(quizzes, 1): #lists all quizzes
                    print(f"{i}. {quiz_file}") 

                selection = int(input("Select quiz number: ")) #takes input
                if 1 <= selection <= len(quizzes): #validation for input
                    current_quiz = os.path.join("quizzes", quizzes[selection - 1]) #changes path to selected
                    print("Selected quiz:", quizzes[selection - 1])
                else:
                    print("Invalid selection.")

        case "3": #case for new quiz
            filename = input("Enter new quiz filename: ").strip() #input
            if filename == "": #validation for input
                print("Filename cannot be empty.")
            else:
                manager.create_quiz(filename) #creates quiz

        case "4": #case for play quiz
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                quiz = manager.load_quiz(current_quiz)
                score = quiz.run()
                name = input("Enter your name for the scoreboard: ")
                if(name.strip() == ""):
                    name = "Anonymous"
                scoreboard.save_score(name, score)

        case "5":
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                manager.list_questions(current_quiz)

        case "6":
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                text = input("Enter question text: ")
                options = input("Enter options separated by commas: ").split(",")
                options = [option.strip() for option in options]
                answer = input("Enter the correct answer: ")

                question = Question(text, options, answer)
                manager.add_question(current_quiz, question)

        case "7":
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                number = int(input("Enter question number to remove: "))
                manager.remove_question(current_quiz, number)

        case "8":
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                text = input("Enter new question text: ")
                options = input("Enter options separated by commas: ").split(",")
                options = [option.strip() for option in options]
                answer = input("Enter the correct answer: ")

                question = Question(text, options, answer)
                number = int(input("Enter question number to update: "))
                manager.update_question(current_quiz, number, question)

        case "9":
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                scoreboard.display_scoreboard()
 
        case "10":
            print("Goodbye!")
            break
            
        case _:
            print("Invalid choice")