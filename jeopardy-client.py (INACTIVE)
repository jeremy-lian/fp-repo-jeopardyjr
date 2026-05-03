from socket32 import create_new_socket

HOST = '127.0.0.1'
PORT = 65432

def buzz_now():
    # keeps asking until the person actually types b to buzz in
    while True:
        ans = input("Type 'b' to buzz: ").strip().lower()
        if ans == 'b':
            return 'B'
        print("Please type 'b' to buzz.")

def get_answer():

    return input('Your answer: ').strip()

def main():
    print('## Welcome to Trivia Buzzer ##')

    with create_new_socket() as s:
        # connect to the server first
        s.connect(HOST, PORT)

        while True:
            #wait for the next message
            msg = s.recv()

            #if server disconnects, stop
            if msg == '':
                break

            #first character tells us what kind of message this is
            header = msg[0]
            body = msg[1:]

            if header == 'Q':
                #server sent a question
                print('\nQUESTION:')
                print(body)

                #let the server know we received it
                s.sendall('OK')

            elif header == 'B':
                #server says buzzing is open
                print(body)

                #send back B if the player buzzes
                s.sendall(buzz_now())

            elif header == 'A':
                #this means playet gets to pick an answer
                print(body)
                answer = get_answer()

                #send answer back with A in front so server knows what it is
                s.sendall('A' + answer)

            elif header == 'R':
                #result of the answer
                print(body)

                #acknowledge the server
                s.sendall('OK')

            elif header == 'G':
                #game/round is over
                print(body)
                s.sendall('OK')
                break

if __name__ == '__main__':
    main()
