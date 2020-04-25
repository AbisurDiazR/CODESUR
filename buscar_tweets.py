# get old tweets
import GetOldTweets3 as got
import json
import sys
# progrees time
import time
# librerias de las interfaces
import tkinter as tk
import tweepy
# web browser lib
import webbrowser
# creacion de documento
from docx import Document
from docx.shared import Inches
# threads
from threading import Thread
from tkinter import CENTER, Entry, Label, LabelFrame, Menu, Tk, ttk
from tkinter.messagebox import showinfo
# archivos
import os
import errno

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
        self.wind.title('BUSCATUIT')

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
        self.button_limpiar = ttk.Button(
            frame, text='Limpiar tabla', command=self.limpiar_tabla)
        self.button_limpiar.grid(row=1, column=3)
        Label(frame, text='Progreso de la busqueda: ').grid(row=2, column=0)
        self.progress_bar = ttk.Progressbar(
            frame, orient='horizontal', length=286, mode='determinate')
        self.progress_bar.grid(row=2, column=1)
        self.label_desc = Label(frame, text='Num Tweets')
        self.label_desc.grid(row=2, column=2)
        self.label_tweets = Label(frame, text='#')
        self.label_tweets.grid(row=2, column=3)

        # creamos la tabla
        self.tree = ttk.Treeview(height=10, columns=(
            'texto', 'autor', 'descripcion', 'location'))
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Id', anchor=CENTER)
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
            # and 'uruguay' in user.location or 'Uruguay' in user.location:
            if len(user.location) != 0:
                self.tree.insert('', 0, text=user.id_str, value=(
                    user.name, user.screen_name, user.description, user.location))
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
            rcmenu.add_command(label='Solo texto', command=self.solo_texto)
            rcmenu.add_command(label='Visitar perfil', command=self.selection)
            rcmenu.add_command(label='Mostrar seguidores',
                               command=self.get_followers)
            rcmenu.post(event.x_root, event.y_root)

    def add_database(self):
        curItem = self.tree.item(self.id_selection)

        path = 'C:/BUSCATUIT/'+curItem['values'][3]+curItem['values'][1]

        showinfo('Guardado iniciado',
                 'Se guardaran los resultados en '+path)

        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        count = 0

        file = open(path+"/"+curItem['values']
                    [1]+".txt", "w", encoding="utf-8")

        try:
            for tweet in tweepy.Cursor(api.user_timeline, user_id=curItem['text'], tweet_mode='extended', include_rts=False).items():
                time.sleep(0.05)
                self.progress_bar["value"] += count
                self.progress_bar.update()
                file.write('Fecha: '+str(tweet.created_at) +
                        ' Texto: '+str(tweet.full_text)+' Ubicacion: '+tweet.user.location+os.linesep)
                print('Trabajando '+str(count))
                self.label_tweets.config(text=str(count))
                count += 1
            self.progress_bar["value"] = 0
        except tweepy.TweepError as e:
            print(e.reason)

        file.close()
        showinfo('Guardado final',
                 'Resultados guardados en '+path)

    def solo_texto(self):
        curItem = self.tree.item(self.id_selection)
        print(curItem['text'])

        path = 'C:/BUSCATUIT/'+curItem['values'][3]+curItem['values'][1]

        showinfo('Guardado iniciado',
                 'Se guardaran los resultados en '+path)

        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        count = 0

        file = open(path+"/"+curItem['values']
                    [1]+"_texto.txt", "w", encoding="utf-8")

        try:
            for tweet in tweepy.Cursor(api.user_timeline, user_id=curItem['text'], tweet_mode='extended', include_rts=False).items():
                time.sleep(0.05)
                self.progress_bar["value"] += count
                self.progress_bar.update()
                if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                    file.write(str(tweet.full_text)+os.linesep)
                    print('Trabajando '+str(count))
                    self.label_tweets.config(text=str(count))
                    count += 1
        except tweepy.TweepError as e:
            print(e.reason)

        file.close()
        showinfo('Guardado final',
                 'Resultados guardados en '+path)

    def get_followers(self):
        count = 0
        curItem = self.tree.item(self.id_selection)
        for follower_id in api.followers(curItem['values'][1]):
            time.sleep(0.05)
            self.progress_bar["value"] += count
            self.progress_bar.update()
            if len(follower_id.location) != 0:
                self.tree.insert('', 0, text=follower_id.id_str, value=(
                    follower_id.name, follower_id.screen_name, follower_id.description, follower_id.location))

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
