### chap05/guess-server.py
import roshambo3_2p_client as rlib
from socket32 import create_new_socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def main():
    #This is only to print who wins at the end
    losses = 0
    wins = 0
    with create_new_socket() as s:
        # Bind socket to address and publish contact info
        s.bind(HOST, PORT)
        s.listen()
        # Updates name --->
        print("RO-SHAM-BO server started. Listening on", (HOST, PORT))

        print('## Welcome to Ro...Sham...BO! ##\nYou are Player #2\n')

        # Define what the choices are
        a = ("rock", "paper", "scissors")

        # Answer incoming connection
        conn2client, addr = s.accept()

        print('Connected by', addr)

        with conn2client:

            while True:   # message processing loop

                # We receive the clients choice (player 1)
                clientchoice = conn2client.recv()

                # If there is no choice, we break out
                if clientchoice == '':
                    break

                # Create a server choice for this connection
                # After we receive an input from the server, we send it all
                serverchoice= rlib.player_choice()

                #Send the server choice
                conn2client.sendall(serverchoice)

                # Once a round is over on the client side, when we have the output, then print it
                result_of_round = conn2client.recv()

                #Added this only to display final message of who won the game
                if "You lose" in result_of_round:
                    losses += 1
                if "You win" in result_of_round:
                    wins += 1

                print(result_of_round)

        if wins == 3:
            print("Congratulations! You Win!\nDisconnected.\n")
        if losses == 3:
            print("You lost. Better luck next time!\nDisconnected.\n")

        # end_of_game = conn2client.recv()
        # print(end_of_game)



if __name__ == '__main__':
    main()

