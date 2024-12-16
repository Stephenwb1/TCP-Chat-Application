# TCP Chat App
https://github.com/user-attachments/assets/9831fd50-9b42-4cfd-9cd9-dc3fcf1cb0b6


In this app, two users can send messages to each other over the internet using the socket interface. First, a server is set up that can receive messages. Then, each user individually starts the program and connects to the server with their own unique
username and port number. After both users have connected, they can send messages to one another via the unix terminal.

In the video above, I have the server running in the top left terminal, user alice in the bottom left, and user bob in the top right.

## Setup

I ran this project on the Mininet VM to simulate a virtual network to test my program on. After installing mininet, ensure that python is installed on the virtual machine, and download all of the "part2" code.

Once the code is set up, open three terminals.

## How to Run

In the first terminal, we will start the server. After users connect, the server is able to run /info to display who is connected.

Start server:

```sh
python3 part2_server.py --port=5000
```

/info :

```sh
/info
```
After the server is started, we start the first user, alice, by running the following commands in the second terminal:

Start user alice:

```sh
python3 part2_client.py --id='alice' --port=9000 --server='127.0.0.1:5000'
```

/id :

```sh
/id
```

/register :

```sh
/register
```

/bridge :

```sh
/bridge
```
After alice, we start user bob in the third terminal, running a similar sequence of commands:

Start user bob:





```sh
python3 part2_client.py --id='bob' --port=9010 --server='127.0.0.1:5000'
```

/id :

```sh
/id
```

/register :

```sh
/register
```

/bridge :

```sh
/bridge
```

/chat :

```sh
/chat
```
At this point, bob can type out anything he likes in the terminal, and it will be sent to alice.
The hosts can chat back and forth, and when they are done, they can ctrl + c or /quit to exit the chat.

## Credit

Credit to Isaac Robles, my partner on this project.\
Completed in CSE 150 - Intro to Computer Networks @ UCSC in Fall 2024
