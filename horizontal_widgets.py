from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView 
# Get Old Tweets
import GetOldTweets3 as got
# Hilos
from threading import Thread
import time
# ttk messagebox


class GroupBox(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(QtCore.QRect(350, 150, 600, 400))
        self.setWindowTitle("CODESUR")
        self.layout = QtWidgets.QGridLayout(self)
        # self.table_tweet = QtWidgets.QTableWidget()

        # primer grupo
        groupbox = QtWidgets.QGroupBox("Buscar en twitter", checkable=False)
        self.layout.addWidget(groupbox)
        # segundo grupo
        groupbox_dos = QtWidgets.QGroupBox("Progreso busqueda", checkable=False)
        self.layout.addWidget(groupbox_dos)
        # tercer grupo
        groupbox_tres = QtWidgets.QGroupBox("Resultados busqueda", checkable=False)
        self.layout.addWidget(groupbox_tres)
        # self.layout.addWidget(self.table_tweet)

        # elementos del primer grupo
        hbox = QtWidgets.QHBoxLayout()
        groupbox.setLayout(hbox)
        label_text = QtWidgets.QLabel("Buscar tweets")
        self.search_text = QtWidgets.QTextEdit()
        self.search_text.setMinimumSize(340, 15)
        self.search_text.setMaximumSize(350, 25)
        button = QtWidgets.QPushButton("Buscar en twitter")
        button.clicked.connect(self.mostrar_tabla)
        hbox.addWidget(label_text, alignment=QtCore.Qt.AlignTop)
        hbox.addWidget(self.search_text, alignment=QtCore.Qt.AlignTop)
        hbox.addWidget(button, alignment=QtCore.Qt.AlignTop)
        hbox.addStretch()
        self.layout.setColumnStretch(1, 1)
        self.layout.setRowStretch(2, 1)

        # elementos del segundo grupo
        hbox_dos = QtWidgets.QHBoxLayout()
        groupbox_dos.setLayout(hbox_dos)
        label_title = QtWidgets.QLabel("Progreso de la busqueda")
        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setGeometry(200, 80, 250, 20)
        #self.progressbar.setMaximum(100)
        hbox_dos.addWidget(label_title, alignment=QtCore.Qt.AlignTop)
        hbox_dos.addWidget(self.progressbar, alignment=QtCore.Qt.AlignTop)
        hbox_dos.addStretch()
        self.layout.setColumnStretch(2,1)
        self.layout.setRowStretch(2,1)

        # elementos del tercer grupo
        hbox_tres = QtWidgets.QHBoxLayout()
        groupbox_tres.setLayout(hbox_tres)
        self.table_tweet = QtWidgets.QTableWidget()
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl("https://twitter.com/"))
        hbox_tres.addWidget(self.table_tweet, alignment=QtCore.Qt.AlignTop)
        hbox_tres.addWidget(self.web_view, alignment=QtCore.Qt.AlignTop)

    def mostrar_tabla(self):
        QMessageBox.information(self,"Busqueda iniciada","Los resultados se cargaran pronto")
        query_tweets = self.search_text.toPlainText()        

        count = 0

        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query_tweets).setSince(
            "2018-05-01").setUntil("2019-05-01").setMaxTweets(100).setNear("Montevideo, Uruguay").setWithin("15mi")
        all_tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        self.progressbar.setMaximum(len(all_tweets))

        # crear el table widget
        #self.table_tweet = QtWidgets.QTableWidget()
        self.table_tweet.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)                
        self.table_tweet.setColumnCount(4)
        self.table_tweet.setRowCount(len(all_tweets))

        # inicializar el encabezado de las columnas
        header = self.table_tweet.horizontalHeader()
        self.table_tweet.setHorizontalHeaderLabels(["Fecha","Texto","Autor","Descripcion del perfil"])

        # inicializar los tooltips del encabezado
        self.table_tweet.horizontalHeaderItem(0)
        self.table_tweet.horizontalHeaderItem(1)
        self.table_tweet.horizontalHeaderItem(2)
        self.table_tweet.horizontalHeaderItem(3)

        # inicializar la alineación de los encabezados
        self.table_tweet.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.table_tweet.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.table_tweet.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)
        self.table_tweet.horizontalHeaderItem(3).setTextAlignment(Qt.AlignCenter)

        # ajustamos el tamaño de las columnas al contenido
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        for tweet in all_tweets:            
            time.sleep(0.05)
            self.progressbar.setValue(count+1)
            date_time = tweet.date.strftime("%m/%d/%Y, %H:%M:%S")
            self.table_tweet.setItem(count,0,QtWidgets.QTableWidgetItem(date_time))
            self.table_tweet.setItem(count,1,QtWidgets.QTableWidgetItem(tweet.text))
            self.table_tweet.setItem(count,2,QtWidgets.QTableWidgetItem(tweet.username))
            self.table_tweet.setItem(count,3,QtWidgets.QTableWidgetItem("https://twitter.com/"+tweet.username))
            count += 1        
        self.table_tweet.move(0, 0)

        #self.layout.addWidget(self.table_tweet)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    screen = GroupBox()
    screen.show()
    sys.exit(app.exec_())
