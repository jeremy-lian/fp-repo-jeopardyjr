import random
import string

DISPLAY_ROWS = ["$100", "$200", "$300", "$400", "$500"]
VALUE_MAP = {
    "$100": "$200",
    "$200": "$400",
    "$300": "$600",
    "$400": "$800",
    "$500": "$1000"
}
NUM_CATEGORIES = 5


def normalize_answer(s):
    s = s.strip().lower()

    for starter in ["what is ", "who is ", "what are ", "who are "]:
        if s.startswith(starter):
            s = s[len(starter):]

    s = s.translate(str.maketrans("", "", string.punctuation))

    words = s.split()
    filler = {"the", "a", "an"}
    words = [w for w in words if w not in filler]

    return " ".join(words)


def normalize_csv_value(value):
    value = value.strip()
    if not value:
        return None

    value = value.replace(",", "").replace(" ", "")

    if not value.startswith("$"):
        return None

    return value


def parse_dollar_value(value_str):
    try:
        return int(value_str.replace("$", "").replace(",", "").strip())
    except ValueError:
        return 0


class Question:
    def __init__(self, text, answer, category, value):
        self.text = text
        self.answer = answer
        self.category = category
        self.value = value
        self.used = False

    def check_answer(self, user_input):
        user = normalize_answer(user_input)
        correct = normalize_answer(self.answer)

        if user == correct:
            return True

        if len(user) >= 4 and (user in correct or correct in user):
            return True

        return False

    def get_points(self):
        return parse_dollar_value(self.value)

    def mark_used(self):
        self.used = True

    def __str__(self):
        return f"[{self.category} - {self.value}] {self.text}"


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, amount):
        self.score += amount


class Board:
    def __init__(self, questions):
        self.questions = questions
        self.categories, self.board = self.build_board_data()

    def build_board_data(self):
        grouped = {}

        for q in self.questions:
            category = q.category
            value = q.value

            if category not in grouped:
                grouped[category] = {}

            if value not in grouped[category]:
                grouped[category][value] = []

            grouped[category][value].append(q)

        valid_categories = []
        needed_values = list(VALUE_MAP.values())

        for category, value_map in grouped.items():
            if all(actual_value in value_map and len(value_map[actual_value]) > 0
                   for actual_value in needed_values):
                valid_categories.append(category)

        if len(valid_categories) < NUM_CATEGORIES:
            raise ValueError("Not enough categories with matching question values.")

        chosen_categories = random.sample(valid_categories, NUM_CATEGORIES)

        board = {}
        for category in chosen_categories:
            board[category] = {}
            for display_value in DISPLAY_ROWS:
                actual_value = VALUE_MAP[display_value]
                board[category][display_value] = random.choice(grouped[category][actual_value])

        return chosen_categories, board
