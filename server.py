import os
import socket
import threading
import json

HOST, PORT = "0.0.0.0", 9999

COMMANDS = {}

def command(action_name):
    def decorator(func):
        COMMANDS[action_name] = func
        return func
    return decorator

@command("next")
def cmd_next(user, request):
    pass

@command("rate")
def cmd_rate(user, request):
    pass

# @command("useless")
# def useless():
#     print("______")

#COMMANDS["next"] = cmd_next так робити не будемо

def handle_client(client_socket, addr):
    user_id = addr[0]
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            request = json.loads(data)
            action = request.get("action") #request["action"]
            #commands?
    except Exception as e:
        print(f"error {e}")
    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"server started on port {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"connected client: {addr}")
        #thread

if __name__=='__main__':
    start_server()