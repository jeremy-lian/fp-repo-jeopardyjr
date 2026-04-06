# CS 32 Final Project Overview --- Multiplayer Jeopardy-Style Game with Live Buzzer System

This project is inspired by client and server programs we have created in the past with the Roshambo game.

# Goal

The main goal of this project is to create a working multiplayer game system with the following features:

- multiple players connect to the same server
- the server stores a database of questions and sends them to the user clients
- the server opens and closes buzzing for each question
- the first player to buzz is selected (will have to figure out how to deal with latency issues)
- the player who buzzed in first gets to answer
- the host on the server (or the server itself) checks whether the answer is correct
- the server updates scores
- the game continues through all the steps until all the questions are used

# Core Files

### 1. Server
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

### 2. Client
Each player will run the game on their own separate clients. It should accomplish the following:
- connect to the server
- send the player's name
- display messages from the server
- allow the player to buzz when the question is fully written out
- allow the player to submit an answer (or just say it verbally without code being used)
- display score updates and results

### 3. Question Database
The game must have a very large set of questions and answers organized into different categories. The questions within these categories should have different point values based on perceived difficulty.



