import tweepy
import json
# librerias de las interfaces
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, LabelFrame, Label, Entry, CENTER, Menu
from tkinter.messagebox import showinfo
# progrees time
import time
import sys
# get old tweets
import GetOldTweets3 as got
# threads
from threading import Thread
# web browser lib
import webbrowser
# creacion de documento
from docx import Document
from docx.shared import Inches

consumer_key = 'gsswiM06At2InB2hgzwfpAiVO'
consumer_secret = 'jvt4RD4s6rzCUbRq4cCQWTS0dwg809TieyIUpPj2kV1UViuqbt'
access_token = '2460423055-aoTaKilqm8RCiwXWXg5d9L0Y3JF6rhVnDA5jpLl'
access_token_secret = '5IuyQNSDleh6PkS1HXSE8N1Au30JgoLhHoj9QtiI3pMhd'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# con este objeto realizaremos todas las llamadas al API
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True, compression=True)

document = Document()


class Ventana:
    id_selection = ' '

    # definimos el metodo que creara la interfaz
    def __init__(self, window):
        self.wind = window
        self.wind.title('CORDESUR')

        # Creamos frame contenedor
        frame = LabelFrame(self.wind, text="Buscar en twitter")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # input busqueda palabra
        Label(frame, text='Buscar palabra: ').grid(row=1, column=0)
        self.name = Entry(frame, width=50)
        self.name.grid(row=1, column=1)
        # botón de busqueda
        self.button = ttk.Button(
            frame, text='Buscar en twitter', command=self.get_twitters)
        self.button.grid(row=1, column=2)
        self.button_limpiar = ttk.Button(frame, text='Limpiar tabla', command=self.limpiar_tabla)
        self.button_limpiar.grid(row=1, column=3)
        Label(frame, text='Progreso de la busqueda: ').grid(row=2, column=0)
        self.progress_bar = ttk.Progressbar(
            frame, orient='horizontal', length=286, mode='determinate')
        self.progress_bar.grid(row=2, column=1)

        # creamos la tabla
        self.tree = ttk.Treeview(height=10, columns=(
            'texto', 'autor', 'descripcion', 'location'))
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Fecha', anchor=CENTER)
        self.tree.heading('texto', text='Texto', anchor=CENTER)
        self.tree.heading('autor', text='Autor', anchor=CENTER)
        self.tree.heading(
            'descripcion', text='Descripcion del perfil', anchor=CENTER)
        self.tree.heading('location', text='Localidad', anchor=CENTER)
        self.tree.bind("<Button-3>", self.popup)

    def get_twitters(self):
        query_word = self.name.get().split()

        t = Thread(target=self.countdown, args=(10, ))

        count = 0

        # fetched_tweets = api.search(self.name.get(), count = 3000) #+ api.search(b, count = 300) + api.search(c, count = 300)
        t.start()
        user_list = api.search_users(query_word)
        for user in user_list:
            time.sleep(0.05)
            self.progress_bar["value"] += count
            self.progress_bar.update()
            if len(user.location) != 0: # and 'uruguay' in user.location or 'Uruguay' in user.location:
                self.tree.insert('', 0, text=user.id_str, value=(user.name, user.screen_name, user.description, user.location))
            count += 1

        self.progress_bar["value"] = 0

    def countdown(self, n):
        showinfo('Por favor espere ',
                 'Busqueda terminada se cargaran los resultados')
        time.sleep(n)

    def popup(self, event):
        # mostrar el popup menu
        rowitem = self.tree.identify('item', event.x, event.y)

        if rowitem == '':
            print('Clic derecho en espacio vacio')
        else:
            # usuario da clic en algo
            print('Seleccion correcta')
            self.tree.selection_set(rowitem)
            # id_selection = self.tree.set(self.tree.identify_row(event.y))
            self.id_selection = rowitem
            rcmenu = Menu(self.tree, tearoff=0)
            # rcmenu.add_command(label='Visitar perfil', command=print(item))
            rcmenu.add_command(label='Añadir a la base de datos',
                               command=self.add_database)
            rcmenu.add_command(label='Visitar perfil', command=self.selection)
            rcmenu.add_command(label='Mostrar seguidores', command=self.get_followers)
            rcmenu.post(event.x_root, event.y_root)

    def add_database(self):
        curItem = self.tree.item(self.id_selection)
        document.add_heading(curItem['values'][0], 0)
        document.add_heading(curItem['values'][1], level=1)
        document.add_paragraph('Descripcion', style='Intense Quote')
        document.add_paragraph(curItem['values'][2])

        count = 0

        for tweet in tweepy.Cursor(api.user_timeline, id=curItem['values'][1]).items():
            time.sleep(0.05)
            self.progress_bar["value"] += count
            self.progress_bar.update()
            document.add_paragraph('ID: '+tweet.id_str+' Fecha: '+str(tweet.created_at) +
                                   ' Texto: '+tweet.text+' Ubicacion: '+tweet.user.location, style='List Number')
            print('Trabajando '+str(count))
            count += 1
        self.progress_bar["value"] = 0

        # document.add_page_break()
        document.save('Registro '+curItem['values'][0]+'.docx')
        print('Tarea completada')

    def get_followers(self):
        count = 0
        curItem = self.tree.item(self.id_selection)
        for follower_id in api.followers(curItem['values'][1]):
            time.sleep(0.05)
            self.progress_bar["value"] += count
            self.progress_bar.update()
            if len(follower_id.location) != 0:
                self.tree.insert('', 0, text=follower_id.id_str, value=(follower_id.name, follower_id.screen_name, follower_id.description, follower_id.location))
            
        self.progress_bar["value"] = 0

    def selection(self):
        curItem = self.tree.item(self.id_selection)
        webbrowser.open_new('https://twitter.com/'+curItem['values'][1])

    def limpiar_tabla(self):
        tree_table = self.tree
        for i in tree_table.get_children():
            self.tree.delete(i)


# metodo main de nuestro programa
if __name__ == "__main__":
    window = Tk()
    application = Ventana(window)
    window.mainloop()
