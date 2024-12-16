import socket
import argparse
import select
import sys

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--server', type=str)
    args = parser.parse_args()
    return [args.id, args.port, args.server]

def valid_args(args):
    if not isinstance(args[1], int):
        print("Invalid arguement for --port, argument must be an int", file=sys.stderr)
        return -1
    elif not isinstance(args[2], str) or ':' not in args[2]:
        print("Invalid arguement for --server, argument must take format 'IP:port_listening_on'", file=sys.stderr)
        return -1
    else:
        return 1

def register_message(clientID, IP, Port, sock):
    message = f"REGISTER\r\nclientID: {clientID}\r\nIP: {IP}\r\nPort: {Port}\r\n\r\n"
    sock.send(message.encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    #print(response)

def bridge_message(clientID, sock):
    #not sure what clientID we should be sending
    message = f"BRIDGE\r\nclientID: {clientID}\r\n\r\n"
    sock.send(message.encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    #parse response into target_ip and target_port, return them
    #print(response)
    return response

def person_two_chat(my_id, my_ip, my_port, target_info): #the second peer

    my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_sock.connect((target_info[1], target_info[2]))
    first_chat = False
    chat = True
    
    while True:
        while chat:
            try:
                chat_message = sys.stdin.readline()
                

                if chat_message.strip() == "/quit":
                    #print("\nTerminating the chat client.\nExiting program")
                    my_sock.sendall("QUIT\r\n".encode('utf-8'))
                    my_sock.close()
                    exit()
                else:
                    #print("bob first")
                    if not first_chat:
                        my_sock.sendall(f"Incoming chat request from {my_id} {my_ip}:{my_port}\n".encode('utf-8'))
                        first_chat = True
                    #print("bob second")
                    my_sock.sendall(chat_message.strip().encode('utf-8'))

                chat = False
                wait = True

            except KeyboardInterrupt:
                #print("\nTerminating the chat client.\nExiting program")
                my_sock.sendall("QUIT\r\n".encode('utf-8'))
                my_sock.close()
                exit()


        while wait:
            #wait for a message
            #when a message is received
            #decode it
            #print alice's message
            #go to chat mode
            #print("you are in wait mode bob")
            #adding this
            
            message = my_sock.recv(1024).decode('utf-8')
            #print(message)

            if message == "Program terminated."or message.strip() == "QUIT":
                    #print("\nTerminating the chat client.\nExiting program")
                    #print("\n")
                    my_sock.close()
                    exit()
            else:
                print(message)
            chat = True
            wait = False

def person_one_chat(my_id, my_ip, my_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_sock:
        address = (my_ip, my_port)
        my_sock.bind(address)
        my_sock.listen(10)
        #print(f"DEBUG: [STARTED] {my_id} is listening on {my_ip}:{my_port}")
        while True:
            client_socket, client_address = my_sock.accept() #accept() gives a WRONG port number, use port variable in the other function
            break

        chat = False        
        wait = True

        message = client_socket.recv(1024).decode('utf-8')
        #print(f"DEBUG: message is = {message}")
        print(message)
        
        first_chat = False

        while True:
            while chat:
                try:
                    #print("DEBUG: you are in chat mode")
                    chat_message = sys.stdin.readline()
                    #print("you are in chat mode alice")

                    chat = False
                    wait = True

                    if chat_message.strip() == "/quit":
                        #print("\nTerminating the chat client.\nExiting program")
                        client_socket.sendall("QUIT\r\n".encode('utf-8'))
                        client_socket.close()
                        my_sock.close()
                        exit()
                    else:
                        client_socket.sendall(chat_message.strip().encode('utf-8'))

                except KeyboardInterrupt:
                    #print("\nTerminating the chat client.\nExiting program")
                    client_socket.sendall("QUIT\r\n".encode('utf-8'))
                    client_socket.close()
                    my_sock.close()
                    exit()

            while wait:
                #print("alice step 1")
                if not first_chat:
                    first_chat = True
                else:
                    #print("alice wait step 2")
                    message = client_socket.recv(1024).decode('utf-8')
                #print(f"DEBUG: message is = {message}")
                    
                #print("alice step 3")
                    if message == "Program terminated." or message.strip() == "QUIT":
                        #print("\nTerminating the chat client.\nExiting program")
                        #print("\n")
                        client_socket.close()
                        exit()
                    else:
                        print(message)
                
                #print("alice step 4")
                chat = True
                wait = False

                


def main():
    jeff = parse_args()
    if valid_args(jeff) == -1:
        return -1
    else:
        target_info = "" #(client_id, ip_address, port)

        valid_commands = ['/id\n', '/register\n', '/bridge\n', '/quit\n', '/chat\n']
        guy = True
        temp = jeff[2].split(':')
        server_IP_Port = (temp[0], int(temp[1]))
        

        #socket connections aren't keep-alive

        
        try:
            print(f"{jeff[0]} running on {temp[0]}:{jeff[1]}")
            while guy:
                input_command = sys.stdin.readline()
                if input_command == valid_commands[0]:
                    sys.stdout.write(jeff[0] + "\n")
                    sys.stdout.flush()
                elif input_command == valid_commands[1]: #register
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(server_IP_Port)
                    register_message(jeff[0], temp[0], jeff[1], sock) #temp[0] is the server's ip which SHOULD be the same as our clients' ip addresses
                    sock.close()

                elif input_command == valid_commands[2]: #bridge
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(server_IP_Port)
                    
                    unparsed_message = bridge_message(jeff[0], sock)
                    lines = unparsed_message.split('\r\n')
                    sock.close()
                    if lines[1] != "clientID:  ": #only run following code if BRIDGEACK isnt empty
                        client_id = str(lines[1].split(': ')[1])
                        ip_address = str(lines[2].split(': ')[1])
                        port = int(lines[3].split(': ')[1])
                        target_info = (client_id, ip_address, port)
                        #print(f"DEBUG: target_info = {target_info}") # we have alice's info
                    else:
                        person_one_chat(jeff[0], temp[0], jeff[1])
                    


                elif input_command == valid_commands[4]: #chat
                    person_two_chat(jeff[0], temp[0], jeff[1], target_info)
                    pass
                elif input_command == valid_commands[3]: #/quit
                    print("\nTerminating the chat client via /quit.\nExiting program")
                    guy = False
                else:
                    print('Invalid Command, Valid Commands are: "/id", "/register", "/bridge", "/quit" ')
        except KeyboardInterrupt:
            exit()
            #print("\nTerminating the client via ctrl + c.\nExiting program")

   
if __name__ == '__main__':
    main()

    