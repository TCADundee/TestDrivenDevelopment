#Main file, allows users to select between playing a quiz, switching quiz, testing or exiting the program.
from quiz.quiz_manager import QuizManager
from quiz.scoreboard import Scoreboard
from quiz.question import Question

manager = QuizManager()
scoreboard = Scoreboard()
current_quiz = "quiz_question.json"
while True:

    print("\n--- Quiz Menu ---")
    print("1. Play Quiz")
    print("2. View Questions")
    print("3. Add Question")
    print("4. Remove Question")
    print("5. Update Question")


    print("7. View Scoreboard")
    print("8. Exit")

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
            manager.list_questions(current_quiz)
        case "3":
            text = input("Enter question text: ")
            options = input("Enter options separated by commas: ").split(",")
            options = [option.strip() for option in options]
            answer = input("Enter the correct answer: ")

            question = Question(text, options, answer)
            manager.add_question(current_quiz, question)
        case "4":
            number = int(input("Enter question number to remove: "))
            manager.remove_question(current_quiz, number)
        case "5":
            text = input("Enter new question text: ")
            options = input("Enter options separated by commas: ").split(",")
            options = [option.strip() for option in options]
            answer = input("Enter the correct answer: ")

            question = Question(text, options, answer)
            number = int(input("Enter question number to update: "))
            manager.update_question(current_quiz, number, question)
        case "6":
            break
        case "7":
            scoreboard.display_scoreboard()
        case "8":
            print("Goodbye!")
            break
        case _:
            print("Invalid choice")