import tkinter as tk
from tkinter import messagebox
import csv
from models import Question, Player, Board, normalize_csv_value

# Values shown on the board
DISPLAY_ROWS = ["$100", "$200", "$300", "$400", "$500"]

# The board has 5 categories and 5 questions per category.
NUM_CATEGORIES = 5
TOTAL_QUESTIONS = NUM_CATEGORIES * len(DISPLAY_ROWS)

def load_questions():
    """
    Load Jeopardy questions from the CSV file and turn and turn each row into 
    a question object.
    """
    questions = []

    with open("JEOPARDY_CSV.csv", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        # remove extra spaces from column names.
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        for row in reader:
            clean_row = {}

            # clean spaces from each key and value in the row
            for key, value in row.items():
                clean_row[key.strip()] = value.strip() if value else ""

            category = clean_row.get("Category", "")
            question = clean_row.get("Question", "")
            answer = clean_row.get("Answer", "")
            value = normalize_csv_value(clean_row.get("Value", ""))

            # Only add the question if all important fields exist
            if category and question and answer and value:
                questions.append(
                    Question(question, answer, category, value)
                )

    return questions

def update_scoreboard(player, answered_count, score_label):
    """
    Uppdate the score label at the bottom of the window
    """
    remaining = TOTAL_QUESTIONS - answered_count
    score_label.config(text=f"Score: {player.score}     Remaining: {remaining}/{TOTAL_QUESTIONS}")
    
def end_game(root, player):
    """
    Show the final score and close the game window.
    """
    messagebox.showinfo("Game Over", f"All questions are done.\nFinal score: {player.score}")
    root.destroy()

def make_question_popup(root, question_obj, button, player, game_state, score_label):
    """
    Create the pop up window that shows one question and answer box
    """
    popup = tk.Toplevel(root)
    popup.title(f'{question_obj.category} - {question_obj.value}')
    popup.geometry("550x320")

    # show the category name
    tk.Label(
        popup,
        text=question_obj.category,
        font=("Arial", 14, "bold"),
        wraplength=500
    ).pack(pady=10)

    # show the question text
    tk.Label(
        popup,
        text=question_obj.text,
        font=("Arial", 12),
        wraplength=500,
        justify="center"
    ).pack(pady=10)

    # Input box where the player types their answer
    entry = tk.Entry(popup, width=40)
    entry.pack(pady=10)

    # label used to show wheter the answer was correct or incorrect
    result_label = tk.Label(
        popup,
        text="",
        wraplength=500,
        font=("Arial", 11)
    )
    result_label.pack(pady=10)

    def check_answer():
        """
        Checl the playes's answer, update the score, and mark the question used.
        """
        # Prevent the same question from being answered twice
        if game_state["done_questions"].get(question_obj, False):
            return

        points = question_obj.get_points()
        user_answer = entry.get()

        # Add points for a correct answer and subtract points for a wrong answer
        if question_obj.check_answer(user_answer):
            result_label.config(text=f"Correct! (+{points})")
            player.add_score(points)
        else:
            result_label.config(text=f"Incorrect. Correct answer: {question_obj.answer} (-{points})")
            player.add_score(-points)

        # Mark  the question as used in both the ibject and the game state
        question_obj.mark_used()
        button.config(state="disabled", text="")
        game_state["done_questions"][question_obj] = True
        game_state["answered"] += 1

        update_scoreboard(player, game_state["answered"], score_label)

        # End the game when evey board question has been answered
        if game_state["answered"] >= TOTAL_QUESTIONS:
            popup.destroy()
            end_game(root, player)
            return

        # Disable the input and cose the popup after a short delay
        entry.config(state="disabled")
        popup.after(1200, popup.destroy)
        
    tk.Button(popup, text="Submit", command=check_answer).pack(pady=10)


def main():
    """
    Set up the full Jeopardy game window
    """
    all_questions = load_questions()

    try:
        # build a randomized board from the loaded questions
        board_obj = Board(all_questions)
        categories = board_obj.categories
        board = board_obj.board
    except ValueError as e:
        # Show an error if the CSV doesnt have enough usable questions
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", str(e))
        return

    root = tk.Tk()
    root.title("Jeopardy Board")

    player = Player("Player 1")
    game_state = {"answered": 0, "done_questions": {}}

    # category headers across the top of the board
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

    update_scoreboard(player, game_state["answered"], score_label)

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
                command=lambda q=qdata, b=btn: make_question_popup(root, q, b, player, game_state, score_label)
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
