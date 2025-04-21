import os
import socket
import threading
import json
import base64

from db import MiniDB

HOST, PORT = "0.0.0.0", 9999

COMMANDS = {}

IMAGES_FOLDER = "beginner_git\\images"
IMAGES_DB ='images.txt'
RATINGS_DB = 'ratings.txt'

CLEAN_ON_START = False

if CLEAN_ON_START:
    open(IMAGES_DB, 'w').close()
    open(RATINGS_DB, 'w').close()

images = MiniDB(['id', 'path'], IMAGES_DB)
ratings = MiniDB(['ip','image', 'rating'], RATINGS_DB)

user_position = {}

def update_user_position(user, shift, default_value):
    total = len(images.data)
    current = user_position.get(user, default_value)
    new_index = (current + shift) %total
    user_position[user] = new_index
    return new_index




def scan_images(path):
    result = []
    for p in os.listdir(path):
        full_path = os.path.join(path, p)
        if os.path.isfile(full_path) and (p.lower().endswith('.png') or p.lower().endswith('.jpg')):
            result.append(full_path)
    return result

if not images.data:
    image_list = scan_images(IMAGES_FOLDER)
    print(image_list)
    id = 1
    for img_path in image_list:
        images.add((id, img_path))
        id += 1


images.save_to_file(IMAGES_DB) 

                                          


def command(action_name):
    def decorator(func):
        COMMANDS[action_name] = func
        return func
    return decorator

def get_image_response(user, record, action):
    image_path = record['path']
    try:
        with open(image_path, 'rb') as img_file:
            image_bytes = img_file.read()
    except Exception as e:
        return {'status':'error', 'error':f'{e}'}
    b64_data = base64.b64encode(image_bytes).decode('utf-8')
    current_rating = 0
    for r in ratings.data:
        if r["ip"] == user and r['image'] == record['id']:
            current_rating = int(r['rating'])
    
    response = {
        'status':'ok',
        'action':action,
        'image':b64_data,
        'id':record['id'],
        'path':image_path,
        'current_rating':current_rating
    }
    return response

@command("get_next")
def cmd_next(user, request):
    index = update_user_position(user, 1, 0)
    record = images.data[index]
    return get_image_response(user, record, "get_next")

@command("get_prev")
def cmd_prev(user, request):
    index = update_user_position(user, -1, 0)
    record = images.data[index]
    return get_image_response(user, record, "get_prev")

@command("rate")
def cmd_rate(user, request):
    image_id = request.get('image')
    ratings_value = request.get('rating')

    if image_id is None or ratings_value is None:
        return {'status':'error', 'error':'id or rating is None'}
    
    rating_found = False
    for r in ratings.data:
        if r['ip'] == user and r['image'] == image_id:
            r['rating'] = ratings_value
            rating_found = True
            break
    
    if not rating_found:
        ratings.add((user, image_id, ratings_value))
    ratings.save_to_file(RATINGS_DB)
    return {'status':'ok', 'action':'rate'}

# @command("useless")
# def useless():
#     print("______")

#COMMANDS["next"] = cmd_next так робити не будемо

def handle_client(client_socket, addr):
    user_id = addr[0]
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return
        request = json.loads(data)
        action = request.get("action") #request["action"]
        if action in COMMANDS:
            response = COMMANDS[action](user_id, request)
        else:
            response = None
        client_socket.send(json.dumps(response).encode())
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
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__=='__main__':
    start_server()