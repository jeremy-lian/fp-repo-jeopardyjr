import tkinter as tk
from tkinter import messagebox
import csv
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
TOTAL_QUESTIONS = NUM_CATEGORIES * len(DISPLAY_ROWS)


def normalize_csv_value(value):
    # clean up the value column so it's always like "$800" or whatever
    value = value.strip()
    if not value:
        return None

    value = value.replace(",", "").replace(" ", "")

    if not value.startswith("$"):
        return None

    return value


def parse_dollar_value(value_str):
    # turn "$800" into 800 so we can do math and pretend we're smart
    try:
        return int(value_str.replace("$", "").replace(",", "").strip())
    except ValueError:
        return 0


def normalize_answer(s):
    # make answers comparable without being annoying about formatting
    s = s.strip().lower()

    # remove Jeopardy starter phrases
    for starter in ["what is ", "who is ", "what are ", "who are "]:
        if s.startswith(starter):
            s = s[len(starter):]

    # delete punctuation (commas, periods, quotes, etc.)
    s = s.translate(str.maketrans("", "", string.punctuation))

    # delete basic filler words
    words = s.split()
    filler = {"the", "a", "an"}
    words = [w for w in words if w not in filler]

    # collapse extra spaces
    return " ".join(words)


def is_correct(user_raw, correct_raw):
    user = normalize_answer(user_raw)
    correct = normalize_answer(correct_raw)

    if user == correct:
        return True

    # "close enough" match (handles first/last name, partial phrasing, etc.)
    if len(user) >= 4 and (user in correct or correct in user):
        return True

    return False


def load_questions():
    questions = []

    with open("JEOPARDY_CSV.csv", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        # Fix headers like " Question" -> "Question"
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        for row in reader:
            clean_row = {}
            for key, value in row.items():
                clean_row[key.strip()] = value.strip() if value else ""

            category = clean_row.get("Category", "")
            question = clean_row.get("Question", "")
            answer = clean_row.get("Answer", "")
            value = normalize_csv_value(clean_row.get("Value", ""))

            if category and question and answer and value:
                questions.append({
                    "Category": category,
                    "Question": question,
                    "Answer": answer,
                    "Value": value
                })

    return questions


def build_board_data(all_questions):
    grouped = {}

    for q in all_questions:
        category = q["Category"]
        value = q["Value"]

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


def update_scoreboard(score_state, score_label):
    # update the scoreboard text so the user can watch their score go up or crash
    remaining = TOTAL_QUESTIONS - score_state["answered"]
    score_label.config(text=f"Score: {score_state['score']}     Remaining: {remaining}/{TOTAL_QUESTIONS}")


def end_game(root, score_state):
    # end the game once all 25 questions are done
    messagebox.showinfo("Game Over", f"All questions are done.\nFinal score: {score_state['score']}")
    root.destroy()


def make_question_popup(root, question_data, button, score_state, score_label):
    popup = tk.Toplevel(root)
    popup.title(f'{question_data["Category"]} - {question_data["Value"]}')
    popup.geometry("550x320")

    tk.Label(
        popup,
        text=question_data["Category"],
        font=("Arial", 14, "bold"),
        wraplength=500
    ).pack(pady=10)

    tk.Label(
        popup,
        text=question_data["Question"],
        font=("Arial", 12),
        wraplength=500,
        justify="center"
    ).pack(pady=10)

    entry = tk.Entry(popup, width=40)
    entry.pack(pady=10)

    result_label = tk.Label(
        popup,
        text="",
        wraplength=500,
        font=("Arial", 11)
    )
    result_label.pack(pady=10)

    answered = {"done": False}

    def check_answer():
        if answered["done"]:
            return

        points = parse_dollar_value(question_data["Value"])

        user_answer = entry.get()
        correct_answer = question_data["Answer"]

        if is_correct(user_answer, correct_answer):
            result_label.config(text=f"Correct! (+{points})")
            score_state["score"] = score_state["score"] + points
        else:
            result_label.config(text=f'Incorrect. Correct answer: {question_data["Answer"]} (-{points})')
            score_state["score"] = score_state["score"] - points

        # mark this square as used
        button.config(state="disabled", text="")
        answered["done"] = True

        # track progress + update scoreboard
        score_state["answered"] = score_state["answered"] + 1
        update_scoreboard(score_state, score_label)

        # if that was the last question, gg
        if score_state["answered"] >= TOTAL_QUESTIONS:
            popup.destroy()
            end_game(root, score_state)
            return

    tk.Button(popup, text="Submit", command=check_answer).pack(pady=10)


def main():
    all_questions = load_questions()

    try:
        categories, board = build_board_data(all_questions)
    except ValueError as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", str(e))
        return

    root = tk.Tk()
    root.title("Jeopardy Board")

    # state stuff for scoring + tracking how many questions are done
    score_state = {"score": 0, "answered": 0}

    # category headers
    for col, category in enumerate(categories):
        header = tk.Label(
            root,
            text=category,
            font=("Arial", 12, "bold"),
            wraplength=140,
            width=15,
            height=3,
            relief="solid",
            bg="lightblue"
        )
        header.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

    # scoreboard row at the bottom
    score_label = tk.Label(
        root,
        text="",
        font=("Arial", 12, "bold"),
        bg="lightgray",
        relief="solid",
        padx=10,
        pady=10
    )
    score_label.grid(row=len(DISPLAY_ROWS) + 1, column=0, columnspan=NUM_CATEGORIES, sticky="nsew", padx=2, pady=2)

    update_scoreboard(score_state, score_label)

    # clue buttons (the actual board)
    for col, category in enumerate(categories):
        for row_index, display_value in enumerate(DISPLAY_ROWS, start=1):
            qdata = board[category][display_value]

            btn = tk.Button(
                root,
                text=display_value,
                width=15,
                height=3
            )

            btn.config(
                command=lambda q=qdata, b=btn: make_question_popup(root, q, b, score_state, score_label)
            )

            btn.grid(row=row_index, column=col, padx=2, pady=2, sticky="nsew")

    # make the grid stretchy
    for col in range(NUM_CATEGORIES):
        root.grid_columnconfigure(col, weight=1)

    for row in range(len(DISPLAY_ROWS) + 2):  # +1 for headers, +1 for scoreboard
        root.grid_rowconfigure(row, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
