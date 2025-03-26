from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

class LikeApp(App):
    def build(self):
        self.mainBox = BoxLayout(orientation="vertical")
        self.lbl_title = Label(text='rate this picture', size_hint=[1, 0.1], font_size=32)
        self.img = Image(source="photo_2024-10-08_16-20-36.jpg")
        btn_layout = BoxLayout(size_hint=[1, 0.2], padding=50, spacing=50)

        btn_like = Button(text="Like", font_size=24, size_hint=[0.45,0.7], padding=50, background_color=[0, 1, 0,1])
        btn_dislike = Button(text="disike", font_size=24, size_hint=[0.45,0.7], padding=50, background_color=[1,0,0,1])

        self.mainBox.add_widget(self.lbl_title)
        self.mainBox.add_widget(self.img)

        btn_layout.add_widget(btn_like)
        btn_layout.add_widget(btn_dislike)

        self.mainBox.add_widget(btn_layout)

        btn_like.bind(on_press=self.like)
        btn_dislike.bind(on_press=self.dislike)

        return self.mainBox

    def like(self, btn):
        print('liked')
    
    def dislike(self, btn):
        print('disliked')

LikeApp().run()