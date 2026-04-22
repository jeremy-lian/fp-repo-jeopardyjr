import csv
import random
from socket32 import create_new_socket

HOST = '127.0.0.1'
PORT = 65432


def load_questions_from_csv():
    questions = []

    with open("JEOPARDY_CSV.csv", newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        for row in reader:
            clean_row = {}
            for key, value in row.items():
                clean_row[key.strip()] = value.strip() if value else ""

            question = clean_row.get("Question", "")
            answer = clean_row.get("Answer", "")
            category = clean_row.get("Category", "")
            value = clean_row.get("Value", "")

            if question and answer and category:
                if not value:
                    value = "$0"

                questions.append({
                    "Question": question,
                    "Answer": answer,
                    "Category": category,
                    "Value": value
                })

    return questions


def send_msg(conn, header, message):
    conn.sendall(header + message)


def recv_msg(conn):
    return conn.recv()


def main():
    questions = load_questions_from_csv()
    print("Loaded", len(questions), "questions")

    if not questions:
        print("No questions found in JEOPARDY_CSV.csv")
        return

    q = random.choice(questions)

    with create_new_socket() as s:
        s.bind(HOST, PORT)
        s.listen()
        print("Jeopardy server started. Listening on", (HOST, PORT))

        conn, addr = s.accept()
        print("Connected by", addr)

        with conn:
            category = q["Category"]
            value = q["Value"]
            question = q["Question"]
            answer = q["Answer"]

            question_line = f"{category} | {value} | {question}"
            send_msg(conn, 'Q', question_line)

            recv_msg(conn)

            send_msg(conn, 'B', "Buzz is open! Type b to buzz.")
            buzz_msg = recv_msg(conn)

            if buzz_msg == 'B':
                send_msg(conn, 'A', "You buzzed first. Enter your answer:")
                answer_msg = recv_msg(conn)

                if answer_msg != '' and answer_msg[0] == 'A':
                    player_answer = answer_msg[1:].strip().lower()
                    correct_answer = answer.strip().lower()

                    if player_answer == correct_answer:
                        send_msg(conn, 'R', f"Correct! You earned {value} points.")
                    else:
                        send_msg(conn, 'R', f"Incorrect. Correct answer: {answer}")

                    recv_msg(conn)

            send_msg(conn, 'G', "Round over.")
            recv_msg(conn)


if __name__ == '__main__':
    main()