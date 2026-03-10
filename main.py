#Main file, allows users to select between playing a quiz, switching quiz, testing or exiting the program.
from quiz.quiz_manager import QuizManager
from quiz.scoreboard import Scoreboard

manager = QuizManager()
scoreboard = Scoreboard()
current_quiz = "C:\\Users\\callu\\OneDrive\\Documents\\GitHub\\TestDrivenDevelopment\\quiz_question.json"
while True:

    print("\n--- Quiz Menu ---")
    print("1. Play Quiz")
    print("2. Modify Quiz")
    print("3. View Scoreboard")
    print("4. Exit")

    choice = input("Choose an option: ")

    match choice:
        case "1":
            quiz = manager.load_quiz(current_quiz)
            score = quiz.run()
            name = input("Enter your name for the scoreboard: ")
            if(name.strip() == ""):
                name = "Anonymous"
            scoreboard.save_score(name, score)
        case "2":
            print("Quiz modification not implemented yet")
            #Placeholder, will allow users to input the filename of the quiz they wish to play, also will be located in the quiz manager.
            current_quiz = input("Enter the filename of the quiz to modify: ")
        case "3":
            scoreboard.display_scoreboard()
        case "4":
            print("Goodbye!")
            break
        case _:
            print("Invalid choice")