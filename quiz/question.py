#Stores all functions relating to the validation and storage of questions in the quiz.
class Question:
    #Default constructor for a question.
    def __init__(self, text, options, answer, qtype="multiple_choice"): #defines the fields of the question
        self.text = text
        self.options = options
        self.answer = answer
        self.qtype = qtype
    def check_answer(self, user_answer): #function to check if user answer is correct.
            return user_answer == self.answer
    
    def ask_question(self):#Ask the question and get user input.

        print("\n" + self.text)
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option}")

        while True:
            try:
                answer_index = int(input("Choose an option: ")) - 1
                if 0 <= answer_index < len(self.options):
                    return self.options[answer_index]
                else:
                    print("Please enter a valid option number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    #Question Verification, added to avoid reusing same code for validating update and add question functions.
    @classmethod
    def validate_question(cls):
        valid_types = ["multiple_choice", "true_false", "multi_select"]
        while True:#Validates question type, looping until a valid type is entered.
            qtype = input(f"Enter question type({', '.join(valid_types)}): ").strip()
            if qtype in valid_types:
                break
            print("Invalid question type. Please try again.")


        while True:#Validates question text, looping until a non-empty question is entered.
            text = input("Enter question text: ").strip()
            if text:
                break
            print("Question text cannot be empty. Please try again.")


        options = []
        if qtype != "true_false": #If not true/false question, validates options.

            while True:#Validates options, looping until at least 2 options are entered.
                options = input("Enter options separated by commas: ").split(",")
                options = [option.strip() for option in options if option.strip()] #removes empty options
                if len(options) >= 2:
                    break
                print("Please enter at least 2 options.")
        

        while True:#Validates answer input, looping until a valid answer is entered.

            if qtype == "multi_select":#Validates multi-select answers.
                answer = input("Enter correct options separated by commas: ").split(",")
                answer = [option.strip() for option in answer if option.strip()]
                if all(option in options for option in answer):
                    break
                print("Please enter valid options for the answer.")

            elif qtype == "true_false":#Validates true/false answer.
                answer = input("Enter correct answer (True/False): ").strip()
                if answer in ["True", "False"]:
                    break
                print("Please enter 'True' or 'False' for the answer.")

            else:#Validates multiple choice answer.
                answer = input("Enter correct option: ").strip()
                if answer in options:
                    break
                print("Please enter a valid option for the answer.")

        question_data = {
            "text": text,
            "options": options,
            "answer": answer,
            "type": qtype
        }

        return Question.create_question(question_data)
        
    #Factory method to create questions based on the type specified. Allowing for easy creation of different question types.
    @staticmethod
    def create_question(data):

        qtype = data.get("type", "multiple_choice") #Default to multiple choice if no type is specified.

        if qtype == "true_false":
            return TrueFalseQuestion(
                data["text"],
                data["answer"]
            )

        elif qtype == "multi_select":
            return MultiSelectQuestion(
                data["text"],
                data["options"],
                data["answer"]
            )

        else:
            return Question(
                data["text"],
                data["options"],
                data["answer"],
                data.get("type", "multiple_choice")
            )
       
#Subclasses for different question types
#Overrides options to be True and False, and only takes the answer as a parameter.
class TrueFalseQuestion(Question):
        def __init__(self, text, answer):
            super().__init__(text, ["True", "False"], answer, qtype="true_false")
    
#Overrides check_answer to handle questions with multiple correct answers.
class MultiSelectQuestion(Question):
        def __init__(self, text, options, answer):
            super().__init__(text, options, answer, qtype="multi_select")

        def check_answer(self, user_answer):
            return set(user_answer) == set(self.answer)
        
        def ask_question(self):
            print("\n" + self.text)
            for i, option in enumerate(self.options, 1):
                print(f"{i}. {option}")

            while True:
                try:
                    answer_indices = input("Choose options separated by commas: ")
                    answer_indices = [int(i.strip()) - 1 for i in answer_indices.split(",")]
                    if all(0 <= index < len(self.options) for index in answer_indices):
                        return [self.options[index] for index in answer_indices]
                    else:
                        print("Please enter valid option numbers.")
                except ValueError:
                    print("Invalid input. Please enter numbers separated by commas.")