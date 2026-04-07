import json
from socket32 import create_new_socket

HOST = '127.0.0.1'
PORT = 65432

def load_questions():
    #retrieve question file
    with open('questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def main():
    #load in the questions
    questions = load_questions()

    # for now just use the first question so this thing actually works
    q = questions[0]

    with create_new_socket() as s:
        #server setup
        s.bind(HOST, PORT)
        s.listen()
        print('Jeopardy server started. Listening on', (HOST, PORT))

        #wait for a client to connect
        conn, addr = s.accept()
        print('Connected by', addr)

        with conn:
            # send the question
            question_line = f"{q['category']} | ${q['value']} | {q['question']}"
            conn.sendall('Q' + question_line)

            #wait for the client to register that it got the question
            conn.recv()

            #allow the client to buzz in
            conn.sendall('B' + 'Buzz is open! Type b to buzz.')

            # grab whatever they send back
            buzz_msg = conn.recv()

            #if player buzzes in
            if buzz_msg == 'B':
                # allow them to answer
                conn.sendall('A' + 'You buzzed first. Enter your answer:')
                answer_msg = conn.recv()

                #make sure the message isn't empty and starts with header A
                if answer_msg != '' and answer_msg[0] == 'A':
                    #clean up the player's answer
                    player_answer = answer_msg[1:].strip().lower()
                    correct_answer = q['answer'].strip().lower()

                    #temporary answer checker
                    if player_answer == correct_answer:
                        conn.sendall('R' + 'Correct! You earned 200 points.')
                    else:
                        conn.sendall('R' + f"Incorrect. Correct answer: {q['answer']}")

                    # wait for the client to acknowledge
                    conn.recv()

            #end the round
            conn.sendall('G' + 'Round over.')
            conn.recv()

if __name__ == '__main__':
    main()
