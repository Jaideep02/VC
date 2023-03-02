from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtGui import QLinearGradient, QColor, QPainter
from PyQt5.QtCore import QTimer
import sys
import speech_recognition as sr
import pyttsx3
import speedtest
import datetime
import openai
import time
import json

class Okno(QMainWindow):
    def __init__(self):
        super(Okno, self).__init__()
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        window_width = screen_size.width() // 2
        window_height = screen_size.height() // 2
        winx = (screen_size.width() - window_width) // 2
        winy = (screen_size.height() - window_height) // 2
        self.setGeometry(winx, winy, 1000, 600)
        self.setWindowTitle("My window")
        self.label = QtWidgets.QLabel()
        self.button1 = QtWidgets.QPushButton()
        self.button2 = QtWidgets.QPushButton()

        self.response = ""
        self.resp = ""
        self.iniUI()

        #Voice assistant functionality
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()


    # Buttons and Label
    def iniUI(self):
        w = QtWidgets.QWidget()
        self.setCentralWidget(w)
        grid = QtWidgets.QGridLayout(w)

        self.counter = 0  # initialize the counter for the typing text animation
        self.typing_timer = QTimer(self)  # create a QTimer for the animation
        self.typing_timer.timeout.connect(self.update_label1_text)  # connect the timer to the update function

        self.scrollArea = QtWidgets.QScrollArea()
        self.label1 = QtWidgets.QLabel()
        self.scrollArea.setWidget(self.label1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(800, 400)
        self.scrollArea.setStyleSheet("background-color: transparent; width:20px; border-radius:20px ")

        self.button1.setText("Activate")
        self.button1.setMinimumWidth(150)
        self.button1.clicked.connect(self.open_file)

        self.button2.setText("Exit")
        self.button2.clicked.connect(self.close)

        self.label.setText("Voice Assistant")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        grid.addWidget(self.label, 0, 35, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        grid.addWidget(self.button1, 1, 8, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        grid.addWidget(self.scrollArea, 3, 6, 4, 60, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        grid.addWidget(self.button2, 10, 70, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        # Connect resizeEvent() to a function that resizes the font sizes
        self.resizeEvent = lambda event: self.on_resize(event)


    def on_resize(self, event):
        w, h = self.width(), self.height()
        if w < 1000 or h < 800:
            font_size1 = 20
            font_size2 = 16
            font_size3 = 14
        else:
            font_size1 = 50
            font_size2 = 20
            font_size3 = 18

        # Resize font sizes for the label and buttons
        self.label.setStyleSheet(f"font-size: {font_size1}px; font-weight: bold; color: white;")
        self.button1.setStyleSheet(f"font-size: {font_size2}px; font-weight: bold; color: white; background-color: transparent; border: 1px solid #f1b30a; border-radius: 5px; cursor: default;")
        self.label1.setStyleSheet(f"font-size: {font_size3}px; color: white; word-wrap: true; letter-spacing: 1px; line-height: {font_size3 + 2}px;")

    def open_file(self):
        self.label1.setText("")  # clear the label text
        self.typing_timer.start(50)  # start the timer with an interval of 1ms
        self.counter = 0  # reset the counter
        self.label1.setWordWrap(True)

        # Listen for the wake word "hey assistant"
        self.engine.say("Listening for wake word...")
        self.engine.runAndWait()
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1) # adjust for ambient noise
            while True:
                audio = self.recognizer.listen(source, timeout=5) # listen for 5 seconds at a time
                try:
                    wake_word = self.recognizer.recognize_google(audio).lower()
                    print("Wake word detected: ", wake_word)
                    if "alexa" in wake_word:
                        self.engine.say("How can I assist you?")
                        self.engine.runAndWait()
                        break
                except sr.UnknownValueError:
                    print("Unknown value error occurred")
                except sr.RequestError as e:
                    print(f"Request error occurred: {e}")

        # Listen for user input
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            self.response = self.recognizer.recognize_google(audio)
            self.resp = "You ~ "+str(self.response)
            self.response = str(self.response)+self.resp+"\n\n"
            print("I'mmm ckkkk ~ ",self.resp)
            self.label1.setText(self.response)
            self.engine.say(self.resp)
            if "speed test" in self.response:
                st = speedtest.Speedtest()
                download_speed = st.download() / 10**6
                upload_speed = st.upload() / 10**6
                self.resp = f"AI ~ The download speed is {download_speed:.2f} Mbps and the upload speed is {upload_speed:.2f} Mbps."
                self.response = str(self.response)+str(self.resp)+"\n\n"
                self.label1.setText(self.response)
                self.engine.say(self.resp)
            # say and print date and time too in gui?
            else:
                # Use OpenAI API to generate text response based on user input
                text = self.response
                openai.api_key = "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"
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=text,
                    temperature=0.7,
                    max_tokens=300
                )
                self.resp = "AI ~ " + response.choices[0].text
                self.response = str(self.response)+str(self.resp)+"\n\n"
                self.label1.setText(self.response)
                self.engine.say(self.resp)
        except sr.UnknownValueError:
            self.engine.say("I am sorry, I could not understand what you said")
        except sr.RequestError:
            self.engine.say("I am sorry, I could not process your request")
                
    def update_label1_text(self):
        # typing text animation
        if self.counter < len(self.response):
            self.label1.setText(self.response[:self.counter])
            self.counter += 1
        else:
            self.typing_timer.stop()


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