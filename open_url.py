import sys

from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
# Tweepy
import tweepy
# Time
import time
# Creacion de carpeta
import os
import errno

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


class Widgets(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("CORDESUR")
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

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.toplayout)
        self.layout.addLayout(self.low_layout)
        self.layout.addWidget(self.webview)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def url_changed(self, url):
        self.url_text.setText(url.toString())
        txt = self.url_text.text()
        self.array = txt.split('/')
        print(self.array)

    def url_set(self):
        self.webview.setUrl(QUrl(self.url_text.text()))

    def get_id(self):
        user = api.get_user(screen_name=self.array[-1])

        self.path = "C:/"+user.location+user.screen_name

        QMessageBox.information(self, "Guardado iniciado",
                                "El archivo se guardara en la carpeta "+self.path)

        try:
            os.mkdir(self.path)
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

        self.path = "C:/"+user.location+user.screen_name

        QMessageBox.information(self, "Guardado iniciado",
                                "El archivo se guardara en la carpeta "+self.path)

        try:
            os.mkdir(self.path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

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




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Widgets()
    window.show()
    sys.exit(app.exec_())
