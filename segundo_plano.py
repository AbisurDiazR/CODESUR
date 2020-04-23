#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton


class Downloader(QThread):

    def __init__(self, url, filename):
        super().__init__()
        self._url = url
        self._filename = filename

    def run(self):
        # Abrir la dirección de URL.
        with urlopen(self._url) as r:
            with open(self._filename, "wb") as f:
                # Leer el contenido y escribirlo en un nuevo archivo.
                f.write(r.read())


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo de descarga de archivo")
        self.resize(400, 300)
        self.label = QLabel("Presione el botón para iniciar la descarga.",
            self)
        self.label.setGeometry(20, 20, 200, 25)
        self.button = QPushButton("Iniciar descarga", self)
        self.button.move(20, 60)
        self.button.pressed.connect(self.initDownload)
    
    def initDownload(self):
        self.label.setText("Descargando archivo...")
        # Deshabilitar el botón mientras se descarga el archivo.
        self.button.setEnabled(False)
        # Ejecutar la descarga en un nuevo hilo.
        self.downloader = Downloader(
            "https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe",
            "python-3.7.2.exe"
        )
        # Qt invocará el método `downloadFinished()` cuando el hilo 
        # haya terminado.
        self.downloader.finished.connect(self.downloadFinished)
        self.downloader.start()
    
    def downloadFinished(self):
        self.label.setText("¡El archivo se ha descargado!")
        # Restablecer el botón.
        self.button.setEnabled(True)
        # Eliminar el hilo una vez que fue utilizado.
        del self.downloader


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()