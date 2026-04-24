import random
import string

# dollar values shown on th board
DISPLAY_ROWS = ["$100", "$200", "$300", "$400", "$500"]

# The CSV uses igher dollar values so this helps us find the actual value
VALUE_MAP = {
    "$100": "$200",
    "$200": "$400",
    "$300": "$600",
    "$400": "$800",
    "$500": "$1000"
}

NUM_CATEGORIES = 5


def normalize_answer(s):
    """
    Clean an answer so user input and correct answers can be compared more fairly.
    """
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
    """
    Clean the dollar value from the CSV and make sure it is usable.
    """
    value = value.strip()
    if not value:
        return None

    value = value.replace(",", "").replace(" ", "")

    if not value.startswith("$"):
        return None

    return value


def parse_dollar_value(value_str):
    """
    Convert a dollar string like "$500" into the integer 500.
    """
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
        """
        Check wheter the player's answer matches the correct answer.
        """
        user = normalize_answer(user_input)
        correct = normalize_answer(self.answer)

        if user == correct:
            return True

        if len(user) >= 4 and (user in correct or correct in user):
            return True

        return False

    def get_points(self):
        """
        Return this the value as an integer.
        """
        return parse_dollar_value(self.value)

    def mark_used(self):
        """
        mark question as chosen
        """
        self.used = True

    def __str__(self):
        return f"[{self.category} - {self.value}] {self.text}"


class Player:
    """
    Represent a player in the game
    """
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, amount):
        self.score += amount


class Board:
    """
    Represents the jeoparsy board
    """
    def __init__(self, questions):
        self.questions = questions
        self.categories, self.board = self.build_board_data()

    def build_board_data(self):
        """
        Group questions by category and value, then choose random categories 
        that have wnough questions to make a full board.
        """
        grouped = {}

        # organize questions
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

        # only valid if it has questions for every neede value
        for category, value_map in grouped.items():
            if all(actual_value in value_map and len(value_map[actual_value]) > 0
                   for actual_value in needed_values):
                valid_categories.append(category)

        if len(valid_categories) < NUM_CATEGORIES:
            raise ValueError("Not enough categories with matching question values.")

        # Pick 5 random categories for this game.
        chosen_categories = random.sample(valid_categories, NUM_CATEGORIES)

        board = {}

        # For each chosen category, choose one random question for each row
        for category in chosen_categories:
            board[category] = {}
            for display_value in DISPLAY_ROWS:
                actual_value = VALUE_MAP[display_value]
                board[category][display_value] = random.choice(grouped[category][actual_value])

        return chosen_categories, board
