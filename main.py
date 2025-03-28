# from kivy import *
# import kivy
from kivy.app import App # головний клас для створення вікна
from kivy.uix.boxlayout import BoxLayout # коробка для дітей (віджетів які потрібно об'єднати)
from kivy.uix.button import Button # кнопка
from kivy.uix.label import Label # звичайний текст
class CafeApp(App):
    def __init__(self):
        App.__init__(self)
        self.dictionary_dishes={"піца карбонара":99,"чай чорний":15,"пончик":25,"не пончик":24,"борщ фрі":33}
        self.number_dish=0 # номер обраної страви
        self.list_dishes=list(self.dictionary_dishes.keys()) # список страв
        self.box_menu=BoxLayout(orientation="vertical") # дозволить відразу відобразити всі віджети
        self.next=Button(text="Наступна страва",font_size=33,on_press=self.change_dish) # створимо кнопку next, яка буде параметром класу
        # on_press викликає вказану функцію при натисканні обраної кнопки
        self.box_menu.add_widget(self.next) # об'єднаємо все в BoxLayout, щоб відразу відобразити
        self.dish=Button(text=(self.list_dishes[self.number_dish]+" за ціною "+str(self.dictionary_dishes[self.list_dishes[self.number_dish]])+" грн"),font_size=33) # створимо кнопку страви
        self.box_menu.add_widget(self.dish) # об'єднаємо все в BoxLayout, щоб відразу відобразити
        self.order=Label(text="Загальна сума замовлення складає 0 грн",font_size=33) # текстова мітка
        self.box_menu.add_widget(self.order) # об'єднаємо все в BoxLayout
        self.previous=Button(text="Попередня страва",font_size=33,on_press=self.change_dish) # створимо кнопку назад
        self.box_menu.add_widget(self.previous) # об'єднаємо все в BoxLayout, щоб відразу відобразити
    def change_dish(self,button): # button - об'єкт кнопки, який буде викликати даний метод
        if button.text=="Наступна страва":
            #self.dish.text="ковбаса"
            self.number_dish=(self.number_dish+1)%len(self.list_dishes) # обираємо наступну страву
            # або переходимо до першої
        elif button.text=="Попередня страва":
            self.number_dish=(self.number_dish-1+len(self.list_dishes))%len(self.list_dishes) # обираємо попередню страву
            # або переходимо до останньої
        self.dish.text=self.list_dishes[self.number_dish]+" за ціною "+str(self.dictionary_dishes[self.list_dishes[self.number_dish]])+" грн" # створимо кнопку страви
    def build(self): # build функція яка наслідується від App та відповідає за створення вікна
        return self.box_menu # повертаємо те, що відображатиме вікно
cafe=CafeApp() # створюємо об'єкт класу
cafe.run() # запускаємо цикл kivy, який працюватиме в окремому потоці даних подібно while True
# та відображатиме вміст об'єкта створеного на основі App
