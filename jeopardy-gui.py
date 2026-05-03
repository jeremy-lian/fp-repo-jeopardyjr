import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import random
from models import Question, Player, Board, normalize_csv_value

# Values shown on the board
DISPLAY_ROWS = ["$100", "$200", "$300", "$400", "$500"]

# The board has 5 categories and 5 questions per category.
NUM_CATEGORIES = 5
TOTAL_QUESTIONS = NUM_CATEGORIES * len(DISPLAY_ROWS)

# Implement difficulty levels for AI "player"
DIFFICULTIES = {
    "Easy": 0.30,
    "Medium": 0.50,
    "Hard": 0.70,
    "Expert": 0.90
}

# Fixes the issue of giving 100 points instead of $100
def display_value_to_points(display_value):
    return int(display_value.replace("$", ""))
def max_wager_for(score):
    #you can always wager at least the top point value (500)
    if score > 500:
        return score
    return 500


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




# Update our scoreboard to now account for AI Player points + User points
def update_scoreboard(player, ai_player, answered_count, score_label):
    remaining = TOTAL_QUESTIONS - answered_count
    score_label.config(
        text=f"Player: {player.score}     AI: {ai_player.score}     Remaining: {remaining}/{TOTAL_QUESTIONS}"
    )




# Display results both for AI and User
def end_game(root, player, ai_player):
    if player.score > ai_player.score:
        winner = "You win!"
    elif ai_player.score > player.score:
        winner = "AI wins!"
    else:
        winner = "It's a tie!"

    messagebox.showinfo(
        "Game Over",
        f"All questions are done.\n\nFinal Score:\nPlayer: {player.score}\nAI: {ai_player.score}\n\n{winner}"
    )
    root.destroy()





# Checking if the game is over, or if the loop should continue
def check_game_over(root, player, ai_player, game_state):
    if game_state["answered"] >= TOTAL_QUESTIONS:
        end_game(root, player, ai_player)
        return True
    return False




# A function defining the AI's turn. This allows us to compete w/ the AI
def ai_turn(root, ai_player, player, game_state, score_label):
    available = [
        clue for clue in game_state["clues"]
        if not game_state["done_questions"].get(clue["question"], False)
    ]

    if not available:
        check_game_over(root, player, ai_player, game_state)
        return

    clue = random.choice(available)
    question_obj = clue["question"]
    button = clue["button"]
    display_value = clue["display_value"]
    points = display_value_to_points(display_value)

    ai_correct = random.random() < game_state["ai_accuracy"]

    if ai_correct:
        ai_player.add_score(points)
        result = (
            f"AI chose {question_obj.category} for {display_value}.\n\n"
            f"AI answered correctly! (+{points})"
        )
    else:
        ai_player.add_score(-points)
        result = (
            f"AI chose {question_obj.category} for {display_value}.\n\n"
            f"AI answered incorrectly. (-{points})\n"
            f"Correct answer: {question_obj.answer}"
        )

    question_obj.mark_used()
    button.config(state="disabled", text="")
    game_state["done_questions"][question_obj] = True
    game_state["answered"] += 1

    update_scoreboard(player, ai_player, game_state["answered"], score_label)

    messagebox.showinfo("AI Turn", result)

    check_game_over(root, player, ai_player, game_state)




def make_question_popup(root, question_obj, button, display_value, player, ai_player, game_state, score_label):

    """
    Create the pop up window that shows one question and answer box
    """
    popup = tk.Toplevel(root)
    popup.title(f'{question_obj.category} - {question_obj.value}')
    popup.geometry("550x320")

    wager_amount = None
    #if the clue is a daily double, then ask for wager before answering
    if getattr(question_obj, "daily_double", False):
        max_wager = max_wager_for(player.score)
        wager_amount = simple.dialog.askinteger(
            "DAILY DOUBLE!",
            f"Daily Double! Enter your wager (1 - {max_wager}):",
            minvalue = 1,
            maxvalue = max_wager,
            parent = popup
        )
    
        #if they cancel, close the popup and don't use the clue
        if wager_amount is None:
            popup.destroy()
            return
            
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
        Check the player's answer, update the score, and mark the question used.
        """
        # Prevent the same question from being answered twice
        if game_state["done_questions"].get(question_obj, False):
            return

        if wager_amount = not None:
            points = wager_amount
        else:
            points = display_value_to_points(display_value)
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

        update_scoreboard(player, ai_player, game_state["answered"], score_label)

        # End the game when evey board question has been answered
        if check_game_over(root, player, ai_player, game_state):
            popup.destroy()
            return

        # Disable the input and cose the popup after a short delay
        entry.config(state="disabled")
        popup.after(1200, popup.destroy)
        root.after(1400, lambda: ai_turn(root, ai_player, player, game_state, score_label))
        
    tk.Button(popup, text="Submit", command=check_answer).pack(pady=10)

'''
Want to be able to select the difficulty level
'''

def show_menu():
    menu = tk.Tk()
    menu.title("Select Difficulty")

    tk.Label(menu, text="Choose Difficulty", font=("Arial", 18)).pack(pady=20)

    def start_game(diff):
        menu.destroy()
        main(diff)

    for diff in DIFFICULTIES:
        tk.Button(
            menu,
            text=diff,
            width=20,
            height=2,
            command=lambda d=diff: start_game(d)
        ).pack(pady=5)

    menu.mainloop()


'''
New input for main() because we want to be able to customize difficulty
'''
def main(difficulty):
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
    root.title(f"Jeopardy Board - Difficulty {difficulty}")

    player = Player("Player 1")
    ai_player = Player("AI")
    game_state = {
        "answered": 0,
        "done_questions": {},
        "clues": [],
        "ai_accuracy": DIFFICULTIES[difficulty]
    }

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

    def restart_game():
        root.destroy()
        show_menu()

    restart_button = tk.Button(
        root,
        text="Restart Game",
        font=("Arial", 12, "bold"),
        command=restart_game
    )

    restart_button.grid(
        row=len(DISPLAY_ROWS) + 2,
        column=0,
        columnspan=NUM_CATEGORIES,
        sticky="nsew",
        padx=2,
        pady=2
    )

    score_label.grid(row=len(DISPLAY_ROWS) + 1, column=0, columnspan=NUM_CATEGORIES, sticky="nsew", padx=2, pady=2)




    update_scoreboard(player, ai_player, game_state["answered"], score_label)

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
                command=lambda q=qdata, b=btn, v=display_value: make_question_popup(root, q, b, v, player, ai_player, game_state, score_label)
            )

            btn.grid(row=row_index, column=col, padx=2, pady=2, sticky="nsew")

            btn.grid(row=row_index, column=col, padx=2, pady=2, sticky="nsew")


            # Tell the AI what is still available
            game_state["clues"].append({
                "question": qdata,
                "button": btn,
                "display_value": display_value,
                "category": category
            })

    # make the grid stretchy
    for col in range(NUM_CATEGORIES):
        root.grid_columnconfigure(col, weight=1)

    for row in range(len(DISPLAY_ROWS) + 3):  # +1 for headers, +1 for scoreboard
        root.grid_rowconfigure(row, weight=1)



    root.mainloop()


if __name__ == "__main__":
    show_menu()
