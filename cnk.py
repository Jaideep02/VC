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

        # Ask the user to say something
        self.engine.say("How can I assist you?")
        self.engine.runAndWait()

        # Listen for user input
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            self.response = self.recognizer.recognize_google(audio)
            self.label1.setText(self.response)
            self.engine.say(self.response)
            if "speed test" in self.response:
                st = speedtest.Speedtest()
                download_speed = st.download() / 10**6
                upload_speed = st.upload() / 10**6
                self.resp = f"The download speed is {download_speed:.2f} Mbps and the upload speed is {upload_speed:.2f} Mbps."
                self.response = self.response+str(self.resp)
                self.label1.setText(self.response)
                self.engine.say(self.resp)
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
                self.resp = str(response['choices'][0]['text']).strip('\n\n')
                self.response = self.response+str(self.resp)
                self.label1.setText(self.response)
                self.engine.say(self.resp)
        except sr.UnknownValueError:
            self.resp = "Sorry, I did not understand that"
            self.response = self.response+str(self.resp)
            self.label1.setText(self.response)
            self.engine.say(self.resp)
        except sr.RequestError as e:
            self.response = "Sorry, my speech service is down"
            self.label1.setText(self.response)
            self.engine.say(self.response)
                
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

'''
    def speak(text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()


    def listen() -> str:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

    def process_command(command: str) -> None:
        if "internet speed" in command:
            st = speedtest.Speedtest()
            download_speed = st.download() / 10 ** 6
            upload_speed = st.upload() / 10 ** 6
            ping_speed = st.results.ping
            speak(f"My internet speed is Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps, Ping: {ping_speed:.2f} ms")
        elif "time" in command:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")
        elif "calculate" in command:
            query = command.replace("calculate", "")
            try:
                result = str(eval(query))
                speak(f"The result is {result}")
            except:
                speak("Sorry, I could not perform the calculation.")
        elif "define" in command:
            query = command.replace("define", "")
            try:
                openai.api_key = "your_api_key_here"
                response = openai.Completion.create(
                engine="davinci",
                prompt=f"Define {query}",
                temperature=0.7,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
                definition = response.choices[0].text
                speak(f"The definition of {query} is {definition}")
            except:
                speak("Sorry, I could not find a definition for that.")
        else:
            speak("Sorry, I did not understand the command.")

    def activate() -> None:
        self.speak("How can I help you?")
        command = self.listen().lower()
        self.process_command(command)
'''
    


def window():
    app = QApplication(sys.argv)
    okno = Okno()
    okno.show()
    sys.exit(app.exec_())

window()