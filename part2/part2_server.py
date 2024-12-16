import socket
import argparse
import select
import sys
import threading

#dictonary to store clients-> name : (ip, port) pairs
client_dict = {}
client_lock = threading.Lock() #to handle user iputs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    return args.port

#global variable
server_port = int(parse_args())
server_ip = "127.0.0.1"

def connect_to_client(client_socket, client_address):
    try:
        while True:
            #check for /info


            data = client_socket.recv(1024).decode('utf-8')
            lines = data.split('\r\n')
            #print(f"DEBUG: lines = {lines}")
            

            if not data:
                break
            #if REGISTER
            if data.startswith("REGISTER"):
                client_id = str(lines[1].split(': ')[1])
                ip_address = str(lines[2].split(': ')[1])
                port = int(lines[3].split(': ')[1])
                

                if client_id not in client_dict:
                    client_dict[client_id] = (ip_address, port)
                    client_socket.sendall(f"REGACK\r\nclientID: {client_id}\r\nIP: {ip_address}\r\nPort: {port}\r\nStatus: registered".encode('utf-8'))
                    print(f'REGISTER {client_id} from {ip_address}:{port} received')
                else:
                    client_socket.sendall(f"{client_id} is already registered.".encode('utf-8'))            
            
            elif data.startswith("BRIDGE"):
               # if len(client_dict.keys()) == 1:
                    #client_socket.sendall(f"{client_id} has already sent a bridge request.".encode('utf-8'))
               # else:
                    client_id = str(lines[1].split(': ')[1])
                    #if THIS client has already registered
                    if client_id in client_dict:
                        first_target = next(iter(client_dict))
                        #pulls the first entry from the dict and feeds the address to target_address
                        target_ip, target_port = client_dict[first_target]
                        my_ip, my_port = client_dict[client_id] 
                        #print(f"DEBUG: target_ip, target_port = {target_ip}, {target_port}")
                        #print(f"DEBUG: my_ip, my_port = {my_ip}, {my_port}")

                        #return the BRIDGEACK to the client
                        if len(client_dict.keys()) == 1:
                            first_target = " "
                            target_ip = " "
                            target_port = " "
                        client_socket.sendall(f"BRIDGEACK\r\nclientID: {first_target}\r\nIP: {target_ip}\r\nPort: {target_port}".encode('utf-8'))
                        

                        #construct the response
                        #BRIDGE: bob 127.0.0.1:9001 alice 127.0.0:8990 example
                        if len(client_dict.keys()) == 2:
                            response = f"BRIDGE: {first_target} {target_ip}:{target_port} {client_id} {my_ip}:{my_port}" 
                            print(response)

            else:
                client_socket.sendall("Error unknown command".encode('utf-8'))
    except Exception as e:
        print(f"[Error] {e}")
    
    finally:
        client_socket.close()


def start_server(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        address = (server_ip, server_port)
        server_socket.bind(address)
        server_socket.listen(10)
        print(f"[STARTED] Server is listening on {server_ip}:{server_port}")
        while True:
            client_socket, client_address = server_socket.accept() #accept() gives a WRONG port number, use port variable in the other function
            threading.Thread(target=connect_to_client, args=(client_socket, client_address)).start()

def handle_user_input():
    while True:
        user_input = input()
        if user_input.strip() == "/info":
            with client_lock:
                for i in range(len(client_dict.keys())):
                    keys = list(client_dict.keys())
                    id = keys[i]
                    ip, port = client_dict[id]
                    print(f"{id} {ip}:{port}")



def main():

    server_thread = threading.Thread(target=start_server, args=(server_ip, server_port))
    server_thread.daemon = True  
    server_thread.start()
    
    handle_user_input()
    
if __name__ == '__main__':
    main()