#Stores functions to manage the quiz, including loading a quiz ,as well as modifying, adding and removing questions.

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