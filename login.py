from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QTableWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
# Tweepy
import tweepy
# Time
import time
# Creacion de carpeta
import sys
import os
import errno
# base de datos
import sqlite3
# tkinter
from tkinter import ttk
from tkinter import *

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# con este objeto realizaremos todas las llamadas al API
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True, compression=True)


class GetTweets(QThread):

    def __init__(self, user, path):
        super().__init__()
        self.user = user
        self.path = path

    # create counter thread
    change_value = pyqtSignal(int)

    def run(self):

        count = 0

        file = open(self.path+"/"+self.user.screen_name +
                    ".txt", "w", encoding='utf-8')

        try:
            for tweet in tweepy.Cursor(api.user_timeline, user_id=self.user.id, tweet_mode='extended', include_rts=False).items():
                time.sleep(0.05)
                
                if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                    file.write("Fecha: "+str(tweet.created_at)+" Texto: " +
                            str(tweet.full_text)+" Localizacion: "+tweet.user.location+os.linesep)
                    print('Trabajando '+str(count))
                    # print('Mostrando '+tweet.full_text)
                    self.change_value.emit(count)
                    count += 1
        except tweepy.TweepError as e:
            print(e.reason)

        file.close()

class OnlyText(QThread):

    def __init__(self, user, path):
        super().__init__()
        self.user = user
        self.path = path

    # create counter thread
    change_value = pyqtSignal(int)

    def run(self):
        count = 0

        file = open(self.path+"/"+self.user.screen_name +
                    "_texto.txt", "w", encoding='utf-8')

        try:
            for tweet in tweepy.Cursor(api.user_timeline, user_id=self.user.id, tweet_mode='extended', include_rts=False).items():
                time.sleep(0.05)
                
                if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                    file.write(str(tweet.full_text) + os.linesep)
                    print('Trabajando '+str(count))
                    # print('Mostrando '+tweet.full_text)
                    self.change_value.emit(count)
                    count += 1
        except tweepy.TweepError as e:
            print(e.reason)

        file.close()                    


class TablaUsuarios(QMainWindow):
    
    db = 'calatuit.db'

    # rol_usuario = ''

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Panel de usuarios")
        self.widget = QWidget(self)

        # nombre de usuario
        self.user_label = QtWidgets.QLabel("Usuario: ")
        self.user_field = QtWidgets.QLineEdit()

        # layout usuario
        self.user_layout = QHBoxLayout()
        self.user_layout.addWidget(self.user_label)
        self.user_layout.addWidget(self.user_field)

        # contraseñas 
        self.pass_label = QtWidgets.QLabel("Contraseña: ")
        self.pass_field = QtWidgets.QLineEdit()

        # layout contraseñas
        self.pass_layout = QHBoxLayout()
        self.pass_layout.addWidget(self.pass_label)
        self.pass_layout.addWidget(self.pass_field)

        # roles
        self.roles_label = QtWidgets.QLabel("Roles: ")
        self.roles = QtWidgets.QComboBox()
        self.roles.addItems(["usuario","administrador"])

        # layout roles
        self.roles_layout = QHBoxLayout()
        self.roles_layout.addWidget(self.roles_label)
        self.roles_layout.addWidget(self.roles)

        # botones
        self.registrar_btn = QtWidgets.QPushButton("Registrar usuario")
        self.registrar_btn.clicked.connect(self.nuevo_usuario)
        self.actualizar_btn = QtWidgets.QPushButton("Editar usuario")
        self.actualizar_btn.clicked.connect(self.editar_usuario)
        self.borrar_btn = QtWidgets.QPushButton("Borrar usuario")
        self.borrar_btn.clicked.connect(self.borrar_usuario)
        self.update_btn = QtWidgets.QPushButton("Actualizar")
        self.update_btn.clicked.connect(self.update_usuario)
        self.update_btn.setEnabled(False)

        # layout botones
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.registrar_btn)
        self.buttons_layout.addWidget(self.actualizar_btn)
        self.buttons_layout.addWidget(self.borrar_btn)
        self.buttons_layout.addWidget(self.update_btn)

        # tabla de usuarios
        self.table_users = QTableWidget()
        self.table_users.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_users.setColumnCount(3)
        self.get_usuarios()
        
        # body_layout
        self.body_layout = QVBoxLayout()
        self.body_layout.addLayout(self.user_layout)
        self.body_layout.addLayout(self.pass_layout)
        self.body_layout.addLayout(self.roles_layout)
        self.body_layout.addLayout(self.buttons_layout)
        self.body_layout.addWidget(self.table_users)
        

        self.widget.setLayout(self.body_layout)
        self.setCentralWidget(self.widget)

    def update_usuario(self):
        try:
            query = "UPDATE usuarios SET nombre_usuario=?, passwd_usuario=?, rol_usuario=? WHERE id_usuario=?"
            parameters = (self.user_field.text(), self.pass_field.text(), self.roles.currentText(), self.id_edit)    
            self.run_query(query, parameters)
        except sqlite3.ProgrammingError as e:
            print('Error encontrado')
            return
        self.user_field.setText('') 
        self.pass_field.setText('')   
        self.update_btn.setEnabled(False)
        self.get_usuarios()

    def editar_usuario(self):
        fila = self.table_users.currentRow()

        try:
            self.table_users.item(fila,0).text()
        except AttributeError as e:
            QMessageBox.information(self,'Atencion','Seleccione un elemento de la tabla')
            return
        
        self.id_edit = self.table_users.item(fila,0).text()
        query_show = "SELECT nombre_usuario, passwd_usuario FROM usuarios WHERE id_usuario="+self.id_edit
        db_rows = self.run_query(query_show)
        usuarios = [dict(nombre_usuario=row[0], passwd_usuario=row[1]) for row in db_rows.fetchall()]        

        for usuario in usuarios:
            self.user_field.setText(usuario['nombre_usuario'])
            self.pass_field.setText(usuario['passwd_usuario'])
        self.update_btn.setEnabled(True)       

    def borrar_usuario(self):
        row = self.table_users.currentRow()

        try:
            self.table_users.item(row,0).text()
        except AttributeError as e:
            QMessageBox.information(self,'Atencion','Seleccione un elemento de la tabla')
            return

        id_delete = self.table_users.item(row,0).text()
        query_delete = "DELETE FROM usuarios WHERE id_usuario = ?"
        self.run_query(query_delete,(id_delete,))
        QMessageBox.information(self,'Borrado','El usuario se ha borrado con exito')
        self.get_usuarios()       


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()

        return result

    def nuevo_usuario(self):
        query = "INSERT INTO usuarios(id_usuario, nombre_usuario, passwd_usuario, rol_usuario) VALUES(NULL,?,?,?)"
        parameters = (self.user_field.text(), self.pass_field.text(), self.roles.currentText())
        self.run_query(query,parameters)
        self.user_field.setText('')
        self.pass_field.setText('')
        self.get_usuarios() 
   
    def get_usuarios(self):
        query = "SELECT id_usuario, nombre_usuario, rol_usuario FROM usuarios"
        db_rows = self.run_query(query)
        usuarios = [dict(id_usuario=row[0], nombre_usuario=row[1], rol_usuario=row[2]) for row in db_rows.fetchall()]
        
        count = 0
        
        print(len(usuarios))
        self.table_users.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_users.setRowCount(len(usuarios))

        # Inicializar el encabezado de las columnas
        header = self.table_users.horizontalHeader()
        self.table_users.setHorizontalHeaderLabels(["Id","Usuario","Rol"])        

        # inicializar los tooltip del encabezado
        self.table_users.horizontalHeaderItem(0)
        self.table_users.horizontalHeaderItem(1)
        self.table_users.horizontalHeaderItem(2)

        # ajustamos el tamaño de las columnas al contenido
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)

        for usuario in usuarios:
            self.table_users.setItem(count,0,QtWidgets.QTableWidgetItem(str(usuario['id_usuario'])))
            self.table_users.setItem(count,1,QtWidgets.QTableWidgetItem(usuario['nombre_usuario']))
            self.table_users.setItem(count,2,QtWidgets.QTableWidgetItem(usuario['rol_usuario']))
            count += 1
        self.table_users.move(0,0)        

class Widgets(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("CALATUIT")
        self.widget = QWidget(self)

        # Widget para el navegador
        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://twitter.com"))
        self.webview.urlChanged.connect(self.url_changed)

        # Ir hacia atras
        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.webview.back)

        # Ir hacia adelante
        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.webview.forward)

        # Actualizar la pagina
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.webview.reload)

        # Barra de direcciones
        self.url_text = QLineEdit()

        # Cargar la pagina actual
        self.go_button = QPushButton("Buscar")
        self.go_button.clicked.connect(self.url_set)

        # Obtener id del usuario
        self.id_button = QPushButton("Obtener Tweets")
        self.id_button.clicked.connect(self.get_id)

        # Solo texto
        self.only_text = QPushButton("Solo texto")
        self.only_text.clicked.connect(self.get_text)

        # progressbar
        self.label_title = QtWidgets.QLabel("Progreso:")
        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setGeometry(200, 80, 250, 20)
        self.label_descripcion = QtWidgets.QLabel("Tweets obtenidos:")
        self.label_tweet = QtWidgets.QLabel("#")

        # botono de administrador
        self.boton_admin = QPushButton("Administra Usuarios")
        self.boton_admin.clicked.connect(self.abrir_usuarios)
        self.dialogs = list()

        self.toplayout = QHBoxLayout()
        self.toplayout.addWidget(self.back_button)
        self.toplayout.addWidget(self.forward_button)
        self.toplayout.addWidget(self.refresh_button)
        self.toplayout.addWidget(self.url_text)
        self.toplayout.addWidget(self.go_button)
        self.toplayout.addWidget(self.id_button)
        self.toplayout.addWidget(self.only_text)

        self.low_layout = QHBoxLayout()
        self.low_layout.addWidget(self.label_title)
        self.low_layout.addWidget(self.progressbar)
        self.low_layout.addWidget(self.label_descripcion)
        self.low_layout.addWidget(self.label_tweet)

        # layout administrador
        self.admin_layout = QHBoxLayout()
        self.admin_layout.addWidget(self.boton_admin)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.toplayout)
        self.layout.addLayout(self.low_layout)
        self.layout.addLayout(self.admin_layout)
        self.layout.addWidget(self.webview)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def abrir_usuarios(self):
        dialog = TablaUsuarios()
        self.dialogs.append(dialog)
        dialog.show()

    def url_changed(self, url):
        self.url_text.setText(url.toString())
        txt = self.url_text.text()
        self.array = txt.split('/')
        print(self.array)

    def url_set(self):
        self.webview.setUrl(QUrl(self.url_text.text()))

    def get_id(self):
        user = api.get_user(screen_name=self.array[-1])

        self.path = "C:/CALATUIT/"+user.location+user.screen_name

        QMessageBox.information(self, "Guardado iniciado",
                                "El archivo se guardara en la carpeta "+self.path)

        try:
            os.makedirs(self.path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self.id_button.setEnabled(False)
        self.only_text.setEnabled(False)
        self.get_tweets = GetTweets(user=user, path=self.path)
        self.get_tweets.change_value.connect(self.progressbar_value)
        self.get_tweets.finished.connect(self.finish_work)
        self.get_tweets.start()

    def finish_work(self):
        print('Tarea terminada')
        self.id_button.setEnabled(True)
        self.only_text.setEnabled(True)
        QMessageBox.information(
            self, "Guardado completado", "Archivo guardado en disco local "+self.path)
        del self.get_tweets

    def progressbar_value(self, val):
        self.label_tweet.setText(str(val))
        self.progressbar.setValue(val)

    def get_text(self):
        user = api.get_user(screen_name=self.array[-1])

        self.path = "C:/CALATUIT/"+user.location+user.screen_name

        QMessageBox.information(self, "Guardado iniciado",
                                "El archivo se guardara en la carpeta "+self.path)

        try:
            os.makedirs(self.path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            return

        self.only_text.setEnabled(False)
        self.id_button.setEnabled(False)
        self.get_texto = OnlyText(user=user, path=self.path)
        self.get_texto.change_value.connect(self.progressbar_value)
        self.get_texto.finished.connect(self.finish_text)
        self.get_texto.start()

    def finish_text(self):
        print('Tarea terminada')
        self.only_text.setEnabled(True)
        self.id_button.setEnabled(True)
        QMessageBox.information(
            self, "Guardado completado", "Archivo guardado en disco local "+self.path)
        del self.get_texto

class Login(QMainWindow):

    dbName = 'calatuit.db'

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("CALATUIT")
        self.widget = QWidget(self)

        # nombre de usuario
        self.user_label = QtWidgets.QLabel("Usuario: ")
        self.user_field = QtWidgets.QLineEdit()

        # layout usuario
        self.user_layout = QHBoxLayout()
        self.user_layout.addWidget(self.user_label)
        self.user_layout.addWidget(self.user_field)

        # contraseñas 
        self.pass_label = QtWidgets.QLabel("Contraseña: ")
        self.pass_field = QtWidgets.QLineEdit()
        self.pass_field.setEchoMode(QtWidgets.QLineEdit.Password)

        # layout contraseñas
        self.pass_layout = QHBoxLayout()
        self.pass_layout.addWidget(self.pass_label)
        self.pass_layout.addWidget(self.pass_field)

        # botones
        self.login_btn = QtWidgets.QPushButton("Ingresar")
        self.login_btn.clicked.connect(self.inicio_sesion)
        self.dialogs = list()
        self.cancel_btn = QtWidgets.QPushButton("Cancelar")
        self.cancel_btn.clicked.connect(self.cerrar_ventana)

        # layout botones
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.login_btn)
        self.buttons_layout.addWidget(self.cancel_btn)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.user_layout)
        self.layout.addLayout(self.pass_layout)
        self.layout.addLayout(self.buttons_layout)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    # funcion que conecta con la base de datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()    
            result = cursor.execute(query, parameters)
            conn.commit()
        return result    

    def inicio_sesion(self):
        # print(self.pass_field.text())
        query = "SELECT rol_usuario FROM usuarios WHERE passwd_usuario=? AND nombre_usuario=?"
        parameters = (self.pass_field.text(), self.user_field.text())
        db_rows = self.run_query(query, parameters)
        for row in db_rows:
            if 'administrador' in row[0]:
                dialog = Widgets()
                dialog.boton_admin.setEnabled(True)
                self.dialogs.append(dialog)
                self.close()
                dialog.show()
                print(row[0])
            else:
                dialogos = Widgets()
                dialogos.boton_admin.setEnabled(False)
                self.dialogs.append(dialogos)
                self.close()
                dialogos.show()
                print(row[0])    

    def cerrar_ventana(self):
        self.close()    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())