from socket32 import create_new_socket

HOST = '127.0.0.1'
PORT = 65432

#get player names from a user input

#buzzer for user

#main function to send and receive information--- this should also use headers to send messages properly
def main():
    print('## Welcome to Jeopardy Live! ##')

    with create_new_socket() as s:
        s.connect(HOST, PORT)

 

if __name__ == '__main__':
    main()
