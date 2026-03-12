#Main file, allows users to select between playing a quiz, switching quiz, testing or exiting the program.
import os
from quiz.quiz_manager import QuizManager
from quiz.scoreboard import Scoreboard
from quiz.question import Question

manager = QuizManager()
scoreboard = Scoreboard()
current_quiz = None #stores which quiz is currently being used
while True:
    #menu
    print("\n--- Quiz Menu ---") 
    print("1. Play Quiz")
    print("2. Select Quiz")
    print("3. Current Quiz")
    print("4. Create Quiz")
    print("5. View/Modify Current Quiz")
    print("6. View Scoreboard")
    print("7. Exit")

    choice = input("Choose an option: ")

    match choice:
        case "1": #Option to start current quiz and play it.
            if current_quiz is None: #check for if a quiz is selected
                print("Please select a quiz first.")
            else:
                quiz = manager.load_quiz(current_quiz) 
                score = quiz.run() #runs quiz and stores score
                name = input("Enter your name for the scoreboard: ") #Receives user input for scoreboard.
                if(name.strip() == ""):
                    name = "Anonymous"
                scoreboard.save_score(name, score, current_quiz.split(".")[0]) #Saves the score to the scoreboard, with the name and quiz used.
        

        case "2": #Option to select a quiz to play or edit.
            quizzes = manager.list_quizzes()
            if not quizzes: #checks if there are any quizzes.
                print("No quizzes available.")
            else:
                print("\nAvailable quizzes:")
                for i, quiz_file in enumerate(quizzes, 1): #prints a list of all quizzes.
                    print(f"{i}. {quiz_file}") 

                try:
                    selection = int(input("Select quiz number: ")) #Receives user input.
                    if 1 <= selection <= len(quizzes): #validation for input.
                        current_quiz = os.path.join("quizzes", quizzes[selection - 1]) #changes path to selected.
                        print("Selected quiz:", quizzes[selection - 1])
                        scoreboard.set_current_quiz(current_quiz.split(".")[0]) #Sets the current quiz for the scoreboard, allowing it to load and save scores for the correct quiz.
                    else:
                        print("Please enter a valid quiz number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                

        case "3": #Option to show the current loaded file that is being used.
            if current_quiz is None:
                print("No quiz selected.")
            else:
                print("Current quiz:", os.path.basename(current_quiz))


        case "4": #Option to create a new quiz, user names the quiz and it is created in the quizzes folder.
            filename = input("Enter new quiz filename: ").strip() #Receives user input.
            if filename == "": #validation for input
                print("Filename cannot be empty.")
            else:
                manager.create_quiz(filename) #creates quiz

        
        case "5": #Option to modify the current quiz.
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                manager.modify_quiz(current_quiz) #Calls the modify quiz loop, allowing users to make multiple changes without having to return to the main menu each time.


        case "6": #Displays the scoreboard for the current quiz.
            if current_quiz is None:
                print("Please select a quiz first.")
            else:
                scoreboard.display_scoreboard()
 

        case "7": #Exits the program.
            print("Goodbye!")
            break
            
        case _: #Default case for invalid input.
            print("Invalid choice")