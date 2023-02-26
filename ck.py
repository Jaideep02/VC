from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtGui import QLinearGradient, QColor, QPainter
from PyQt5.QtCore import QTimer
import sys


class Okno(QMainWindow):
    def __init__(self):
        super(Okno, self).__init__()
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        window_width = screen_size.width() // 2
        window_height = screen_size.height() // 2
        winx = (screen_size.width() - window_width) // 2
        winy = (screen_size.height() - window_height) // 2
        self.setGeometry(winx, winy, 900, 500)
        self.setWindowTitle("My window")
        self.label = QtWidgets.QLabel()
        self.button1 = QtWidgets.QPushButton()
        self.button2 = QtWidgets.QPushButton()
        self.iniUI()

    # Buttons and Label
    def iniUI(self):
        w = QtWidgets.QWidget()
        self.setCentralWidget(w)
        grid = QtWidgets.QGridLayout(w)

        self.counter = 0  # initialize the counter for the typing text animation
        self.typing_timer = QTimer(self)  # create a QTimer for the animation
        self.typing_timer.timeout.connect(self.update_label1_text)  # connect the timer to the update function
        self.label1 = QtWidgets.QLabel()

        self.label1 = QtWidgets.QLabel()

        self.button1.setText("Activate")
        self.button1.setMinimumWidth(150)
        self.button1.setStyleSheet("font-size: 20px; font-weight: bold; color: white; background-color: transparent; border: 1px solid #f1b30a; border-radius: 5px; cursor: default;")
        self.button1.clicked.connect(self.open_file)

        self.button2.setText("Exit")
        self.button2.clicked.connect(self.close)

        self.label.setText("Voice Assistant")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        grid.addWidget(self.label, 0, 8, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        grid.addWidget(self.button1, 1, 8, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        grid.addWidget(self.label1, 4, 6, 4, 20, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        grid.addWidget(self.button2, 6, 20, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

    def open_file(self):
        self.label1.setText("")  # clear the label text
        self.typing_timer.start(50)  # start the timer with an interval of 50ms
        self.counter = 0  # reset the counter
        self.label1.setWordWrap(True)
        self.label1.setStyleSheet("font-size: 18px; font-weight: bold; color: white; word-wrap: true;")
        
    def update_label1_text(self):
        text = "The law of conservation of charge states that the total electric charge in a closed system remains constant, meaning that charges cannot be created or destroyed but only transferred from one object to another."
        user_text = self.label1.text()  # get the text typed by the user
        if self.counter < len(text):
            self.label1.setText(text[:self.counter+1] + user_text)  # set the label text to include the user's typed text
            self.counter += 1  # increment the counter
        else:
            self.typing_timer.stop()  # stop the timer when the text is fully typed
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(1, 43, 77))
        gradient.setColorAt(1.0, QColor(0, 0, 0))
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

def window():
    app = QApplication(sys.argv)
    okno = Okno()
    okno.show()
    sys.exit(app.exec_())

window()