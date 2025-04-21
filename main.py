from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

import socket
import json
import threading
import base64
import os
import io

HOST, PORT = '127.0.0.1', 9999

def send_request(action, data, callback):
    def worker():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            request = {"action":action}
            if data:
                request.update(data)
            s.sendall(json.dumps(request).encode())
            response_data = b''
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            response = json.loads(response_data.decode())
        except Exception as e:
            response = {"status":"error", "error":f"{e}"}
        finally:
            s.close()
        Clock.schedule_once(lambda c: callback(response))
    threading.Thread(target=worker, daemon=True).start()
        



class LikeApp(App):
    def build(self):
        self.mainBox = BoxLayout(orientation="vertical")
        self.lbl_title = Label(text='rate this picture', size_hint=[1, 0.1], font_size=32)
        self.img = Image(source="photo_2024-10-08_16-20-36.jpg")
        btn_layout = BoxLayout(size_hint=[1, 0.4], padding=50, spacing=50)

        self.current_image_id = 0
        self.current_rating = 0

        self.stars = []

        for i in range(5):
            btn = Button(text = f"{i+1}", 
                         color=[0,0,0,0], 
                         background_normal = "beginner_git/star0.png", 
                         background_down = "beginner_git/star0.png",
                         on_press = self.rate)
            self.stars.append(btn)
            btn_layout.add_widget(btn)


        self.mainBox.add_widget(self.lbl_title)
        self.mainBox.add_widget(self.img)

        self.mainBox.add_widget(btn_layout)
        self.request_image('get_next')

        return self.mainBox

    def rate(self, btn):
        index = int(btn.text) - 1
        for i in range(len(self.stars)):
            if i <= index:
                self.stars[i].background_normal = "beginner_git/star1.png"
                self.stars[i].background_down = "beginner_git/star1.png"
            else:
                self.stars[i].background_normal = "beginner_git/star0.png"
                self.stars[i].background_down = "beginner_git/star0.png"
        self.current_rating = index + 1
    
    def request_image(self, action):
        send_request(action, None, self.on_image_response)
    
    def on_prev(self, btn):
        self.request_image('get_prev')
    
    def on_next(self, btn):
        self.request_image('get_next')
    
    def on_rate(self, btn):
        if self.current_image_id is None or self.current_rating == 0:
            return
        data = {'image':self.current_image_id,'rating':self.current_rating}
        send_request('rate',data, self.on_rate_response)
    
    def on_rate_response(self, response):
        return
    
    def on_image_response(self, response):
        if response.get('status') == 'ok':
            b64_data = response.get('image')
            image_bytes = base64.b64decode(b64_data)
            self.current_image_id = response.get('id')
            self.current_image_path = response.get('path')
            ext = 'png'
            if self.current_image_path:
                ext = os.path.splitext(self.current_image_path)[1][1:].lower()
            data_stream = io.BytesIO(image_bytes)
            core_image = CoreImage(data_stream, ext=ext)
            self.img.texture = core_image.texture
            
            current_rating = response.get('current_rating', 0)

            for i, star in enumerate(self.stars):
                if i < current_rating:
                    star.background_normal = 'beginner_git/star1.png'
                    star.background_down = 'beginner_git/star1.png'
                else:
                    star.background_normal = 'beginner_git/star0.png'
                    star.background_down = 'beginner_git/star0.png'





LikeApp().run()