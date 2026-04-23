import random

class Question:
    def __init__(self, text, answer, category, value):
        self.text = text
        self.answer = answer
        self.category = category
        self.value = value

    def check_answer(self, user_input):
        return user_input.strip().lower() == self.answer.strip().lower()

    def __str__(self):
        return f"[{self.category} - {self.value}] {self.text}"


class Game:
    def __init__(self, questions):
        self.questions = questions
        self.current_question = None

    def get_random_question(self):
        self.current_question = random.choice(self.questions)
        return self.current_question


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, amount):
        self.score += amount
