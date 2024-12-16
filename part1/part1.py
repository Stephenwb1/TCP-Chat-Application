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
    print(response)

def bridge_message(clientID, sock):
    #not sure what clientID we should be sending
    message = f"BRIDGE\r\nclientID: {clientID}\r\n\r\n"
    sock.send(message.encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    print(response)

def main():
    jeff = parse_args()
    if valid_args(jeff) == -1:
        return -1
    else:
        valid_commands = ['/id\n', '/register\n', '/bridge\n', '/quit\n']
        guy = True
        temp = jeff[2].split(':')
        server_IP_Port = (temp[0], int(temp[1]))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_IP_Port)
        try:
            while guy:
                input_command = sys.stdin.readline()
                if input_command == valid_commands[0]:
                    print(jeff[0])
                elif input_command == valid_commands[1]:
                    register_message(jeff[0], temp[0], jeff[1], sock)
                elif input_command == valid_commands[2]:
                    bridge_message(jeff[0], sock)
                elif input_command == valid_commands[3]:
                    sock.close()
                    print("\nTerminating the chat client.\nExiting program")
                    guy = False
                else:
                    print('Invalid Command, Valid Commands are: "/id", "/regiter", "/bridge", "/quit" ')
        except KeyboardInterrupt:
            print("\nTerminating the chat client.\nExiting program")

    #huehrfuisdef 
if __name__ == '__main__':
    main()

    