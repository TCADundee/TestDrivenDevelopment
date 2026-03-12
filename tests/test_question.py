#Stores all tests relating to the questions in the quiz.
from quiz.question import Question

def test_question_correct_answer():
    question = Question("What is the largest desert in the world?",
                         ["Sahara", "Gobi", "Kalahari", "Antarctica"],
                         "Antarctica")
    
    assert question.check_answer("Antarctica"), "Should return True for correct answer"


def test_question_incorrect_answer():
    question = Question("What is the largest desert in the world?",
                         ["Sahara", "Gobi", "Kalahari", "Antarctica"],
                         "Antarctica")

    assert not question.check_answer("Sahara"), "Should return False for incorrect answer"

def test_question_initialization():
    text = "What is 2+2?"
    options = ["3", "4", "5"]
    answer = "4"
    
    question = Question(text, options, answer)
    
    assert question.text == text, "Question text should match input"
    assert question.options == options, "Question options should match input"
    assert question.answer == answer, "Question answer should match input"

def test_question_exact_match_required():
    question = Question("What is the capital of France?",
                         ["Paris", "London", "Berlin"],
                         "Paris")
    
    # Test case sensitivity
    assert not question.check_answer("paris"), "Should be case sensitive (lowercase paris should fail)"
    assert question.check_answer("Paris"), "Should match exact case"

def test_question_check_answer_empty_string():
    question = Question("What is the answer?",
                         ["Yes", "No"],
                         "Yes")
    
    assert not question.check_answer(""), "Empty string should not match correct answer"

def test_question_check_answer_with_spaces():
    question = Question("What is the answer?",
                         ["Answer One", "Answer Two"],
                         "Answer One")
    
    assert question.check_answer("Answer One"), "Should match exact answer with spaces"
    assert not question.check_answer("AnswerOne"), "Should not match if spaces are removed"
    assert not question.check_answer(" Answer One"), "Should not match if trailing space is added"

def test_question_check_answer_special_characters():
    question = Question("What is the symbol?",
                         ["@", "#", "$"],
                         "@")
    
    assert question.check_answer("@"), "Should match special character answer"
    assert not question.check_answer("#"), "Should not match different special character"

def test_question_check_answer_numeric_options():
    question = Question("What is 5 * 5?",
                         ["20", "25", "30"],
                         "25")
    
    assert question.check_answer("25"), "Should match string answer"
    assert not question.check_answer(25), "Should not match integer (type mismatch)"  # Integer != String

def test_question_check_answer_none():
    question = Question("What is the answer?",
                         ["Yes", "No"],
                         "Yes")
    
    assert not question.check_answer(None), "None should not match any answer"

def test_question_with_special_characters_in_text():
    question = Question("What is 2 + 2?",
                         ["3", "4", "5"],
                         "4")
    
    assert question.text == "What is 2 + 2?", "Should preserve special characters in text"
    assert question.check_answer("4"), "Should still evaluate answers correctly"

def test_question_with_multiple_correct_options():
    question = Question("Pick one",
                         ["A", "B", "C"],
                         "B")
    
    assert question.check_answer("B"), "Should match correct answer"
    assert not question.check_answer("A"), "Should not match different option"
    assert not question.check_answer("C"), "Should not match different option"

def test_question_attributes_are_independent():
    q1 = Question("Q1?", ["A", "B"], "A")
    q2 = Question("Q2?", ["X", "Y"], "X")
    
    assert q1.text != q2.text, "Different questions should have different text"
    assert q1.answer != q2.answer, "Different questions should have different answers"
    assert q1.check_answer("A"), "Q1 should accept its answer"
    assert not q1.check_answer("X"), "Q1 should not accept Q2's answer"
    assert q2.check_answer("X"), "Q2 should accept its answer"
    assert not q2.check_answer("A"), "Q2 should not accept Q1's answer"