#Main file, allows users to select between playing a quiz, switching quiz, testing or exiting the program.
from quiz.quiz_manager import QuizManager

manager = QuizManager()
current_quiz = None
while True:

    print("\n--- Quiz Menu ---")
    print("1. Play Quiz")
    print("2. Modify Quiz")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":

        quiz = manager.load_quiz(current_quiz)
        quiz.run()

    elif choice == "2":

        print("Quiz modification not implemented yet")
        #Placeholder, will allow users to input the filename of the quiz they wish to play, also will be located in the quiz manager.
        current_quiz = input("Enter the filename of the quiz to modify: ")

    elif choice == "3":

        print("Goodbye!")
        break

    else:

        print("Invalid choice")