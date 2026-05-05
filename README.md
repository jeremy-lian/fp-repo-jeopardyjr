# CS 32 Final Project Overview --- Singleplayer Jeopardy-Style Game vs AI

This project was originally inspired by client and server programs we have created in the past with the Roshambo game, but was altered to deliver a completely offline singleplayer experience.

# Goal

The main goal of this project is to create a working Jeopardy-style game with the following eatures:

- A 5x5 clickable Jeopardy board built in Tkinter
- A real question database loaded from a large CSV dataset
- Player vs AI gampleay, where the AI answers with a probability based on a selected difficulty
- Score tracking for both the player and AI shown on the board
- Used-square tracking so each question can only be answered once
- Daily double functionality where you can wager points instead of using the clue value
- Final Jeopardy at the end of the board, inclduing wagers and a final winner
- A restart option to generate a new board and start a new game

# Core Files

### 1. Server (INACTIVE)
The server is what the users will connect to through their clients. It should accomplish the following:
- accept client connections
- store player names and connections
- load question data from a large database of questions
- create a screen of all the questions available
- send game updates to the players
- manage buzzing system and decide who buzzed first
- receive player answers and assess correctness (either the server or the host on the server will do this)
- update scores and display to users
- determine if the game should be over

### 2. Client (INACTIVE)
Each player will run the game on their own separate clients. It should accomplish the following:
- connect to the server
- send the player's name
- display messages from the server
- allow the player to buzz when the question is fully written out
- allow the player to submit an answer (or just say it verbally without code being used)
- display score updates and results

### 3. GUI (MAIN GAME)
The jeopardy-gui.py file runs the working offline Jeopardy game. It builds a 5x5 clickable Jeopardy board, supports Player vs AI mode (dificulty based accuracy), tracks scores, disables squares that have been used, and ends automatically once all 25 questions have been used.

### 4. Models / Logic
- 'models.py' holds the main classes and game logic
- 'Question' stores question text/answer/value and implements answer checkign
- 'Board' generates valid categories + values and places Daily Doubles
- 'Player' tracks score and applies scoring updates

### 5. Question Database
The game must have a very large set of questions and answers organized into different categories. The questions within these categories should have different point values based on perceived difficulty.

### How to run
Simply run the Offline GUI to play the working offline single-player Jeopardy game using 'python3 jeopardy-gui.py'
A start screen will appear with instructions followed by options for game difficulty.
After selecting game difficulty, the 5×5 Jeopardy board will load with five randomly chosen categories. You can click any dollar value to open a question, type an answer, and submit. Your score (and the AI’s score) updates on the scoreboard depending on whether or not you get the answer correct, used squares are disabled, and the game ends automatically after all 25 clues are used (followed by Final Jeopardy).


### Testing (specifically what we verified)
- Verified score increases and decreases based on the question value
- Verified that squares cannot be selected more than once
- Verified answer checking works with capitalization/punctuation differences (as well as the close enough feature that is definitely too lenient)
- Verified game will end after 25 questions and shows the final score
- Verified that daily double allows you to wager a value between 1-500
- Verified that final jeopardy allows you to wager any value above 0 (if possible)
  
### Data Sources / References
- Jeopardy question dataset (Kaggle): https://www.kaggle.com/datasets/tunguz/200000-jeopardy-questions
- Tkinter grid reference: https://realpython.com/python-gui-tkinter/

### AI Usage
We used generative AI to accomplish the following:
- brainstorming score tracking and end-of-game logic for the GUI
- implementing the less strict answer matching
- planning the client-server message protocols (inspired by the Roshambo from Pset 3)
- brainstorming how to make the game function as User vs AI

All the AI-inspired code was reviewed by us before and we tested them using the tests mentioned.

# Pivot

### Game Structure
We originally intended to create a multiplayer client-server buzzer game inspired by Roshambo mixed with Jeopardy, but after feedback and difficulty realizations, we pivoted to an offline GUI version against an AI.


