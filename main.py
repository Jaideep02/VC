import sys
import speech_recognition as sr
import pyttsx3
import smtplib
import os
import time
import mysql.connector
import speedtest_cli
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set up wakeword detection
r = sr.Recognizer()
m = sr.Microphone()

def listen():
    with m as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        engine.say("Sorry, I did not understand that.")
        engine.runAndWait()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        engine.say("Could not request results from Google Speech Recognition service")
        engine.runAndWait()


# Function to send email
def send_email(to, subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail('your-email@gmail.com', to, message)
    print("Email sent successfully")
    engine.say("Email sent successfully")
    engine.runAndWait()
    server.quit()

# Function to open application
def open_app(app_name):
    os.system(f"open /Applications/{app_name}.app")
    print(f"{app_name} opened successfully")
    engine.say(f"{app_name} opened successfully")
    engine.runAndWait()

# Function to create MySQL database
def create_db(db_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword"
    )
    mycursor = mydb.cursor()
    mycursor.execute(f"CREATE DATABASE {db_name}")
    print(f"{db_name} database created successfully")
    engine.say(f"{db_name} database created successfully")
    engine.runAndWait()

# Function to create table in MySQL database
def create_table(db_name, table_name, columns):
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database=db_name
    )
    mycursor = mydb.cursor()
    column_defs = ", ".join([f"{column_name} {column_type}" for column_name, column_type in columns.items()])
    mycursor.execute(f"CREATE TABLE {table_name} ({column_defs})")
    print(f"{table_name} table created successfully")
    engine.say(f"{table_name} table created successfully")
    engine.runAndWait()

# Function to perform speedtest


def create_text_file(filename):
    try:
        with open(filename, 'w') as f:
            f.write('')
        print(f"{filename} created successfully")
        engine.say(f"{filename} created successfully")
        engine.runAndWait()
    except Exception as e:
        print(f"Error creating {filename}: {e}")
        engine.say(f"Error creating {filename}")
        engine.runAndWait()

def edit_text_file(filename):
    try:
        with open(filename, 'r') as f:
            contents = f.read()
        print(f"Editing {filename}")
        engine.say(f"Editing {filename}")
        engine.runAndWait()
        with open(filename, 'w') as f:
            new_contents = input("Enter new text: ")
            f.write(new_contents)
        print(f"{filename} updated successfully")
        engine.say(f"{filename} updated successfully")
        engine.runAndWait()
    except Exception as e:
        print(f"Error editing {filename}: {e}")
        engine.say(f"Error editing {filename}")
        engine.runAndWait()

def remind(reminder_text):
    print(f"Reminder: {reminder_text}")
    engine.say(f"Reminder: {reminder_text}")
    engine.runAndWait()

# Function to start and stop a stopwatch using voice commands
def start_stopwatch():
    stopwatch_running = False
    while True:
        command = listen()
        if "start" in command and "stopwatch" in command:
            if not stopwatch_running:
                start_time = time.time()
                print("Stopwatch started")
                engine.say("Stopwatch started")
                engine.runAndWait()
                stopwatch_running = True
            else:
                print("Stopwatch is already running")
                engine.say("Stopwatch is already running")
                engine.runAndWait()
        elif "stop" in command and "stopwatch" in command:
            if stopwatch_running:
                elapsed_time = time.time() - start_time
                print(f"Elapsed time: {elapsed_time:.2f} seconds")
                engine.say(f"Elapsed time: {elapsed_time:.2f} seconds")
                engine.runAndWait()
                stopwatch_running = False
            else:
                print("Stopwatch is not running")
                engine.say("Stopwatch is not running")
                engine.runAndWait()

# GUI setup
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.commandLabel = QtWidgets.QLabel(self.centralwidget)
        self.commandLabel.setGeometry(QtCore.QRect(20, 20, 200, 30))
        self.commandLabel.setText("Command:")

        self.commandLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.commandLineEdit.setGeometry(QtCore.QRect(80, 20, 200, 30))

        self.submitButton = QtWidgets.QPushButton(self.centralwidget)
        self.submitButton.setGeometry(QtCore.QRect(300, 20, 80, 30))
        self.submitButton.setText("Submit")

        self.outputTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.outputTextEdit.setGeometry(QtCore.QRect(20, 60, 360, 200))
        gradient_style = "background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #7f7fd5, stop:1 #86a8e7);"
        self.outputTextEdit.setStyleSheet(gradient_style)
        text_style = "color: white; font-size: 14pt;"
        self.outputTextEdit.setStyleSheet(gradient_style + text_style)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))
        self.submitButton.setText(_translate("MainWindow", "Submit"))

def main():
    # Initialize text-to-speech engine
    engine = pyttsx3.init()

    # GUI setup
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    def run_speedtest():
        st = speedtest_cli.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1000000
        upload_speed = st.upload() / 1000000
        ping = st.results.ping
        print("Download speed: {download_speed} Mbps")
        print("Upload speed: {upload_speed} Mbps")
        print("Ping: {ping} ms")
        ui.outputTextEdit.append(f"Download speed: {download_speed:.2f} Mbps")
        ui.outputTextEdit.append(f"Upload speed: {upload_speed:.2f} Mbps")
        engine.say(f"Download speed is {download_speed} megabits per second. Upload speed is {upload_speed} megabits per second. Ping is {ping} milliseconds.")
        engine.runAndWait()

    def button_click():
        command = ui.commandLineEdit.text()
        ui.outputTextEdit.append(f"\nYou said: {command}")
        if "send email" in command:
            to = input("Enter recipient email: ")
            subject = input("Enter email subject: ")
            body = input("Enter email body: ")
            send_email(to, subject, body)
        elif "open" in command:
            app_name = command[command.index("open")+5:]
            open_app(app_name)
        elif "create database" in command:
            db_name = input("Enter database name: ")
            create_db(db_name)
        elif "create table" in command:
            db_name = input("Enter database name: ")
            table_name = input("Enter table name: ")
            columns = {}
            while True:
                column_name = input("Enter column name (or enter to stop): ")
                if not column_name:
                    break
                column_type = input(f"Enter type for {column_name}: ")
                columns[column_name] = column_type
            create_table(db_name, table_name, columns)
        elif "run speedtest" in command:
            run_speedtest()
        elif "create text file" in command:
            filename = input("Enter filename: ")
            create_text_file(filename)
        elif "edit text file" in command:
            filename = input("Enter filename: ")
            edit_text_file(filename)
        elif "set reminder" in command:
            # Prompt user for reminder details
            print("Sure, what's the reminder?")
            engine.say("Sure, what's the reminder?")
            engine.runAndWait()
            reminder_text = input("Reminder: ")
            print("When do you want to be reminded? (e.g. 'in 5 minutes', 'at 3:30 PM')")
            engine.say("When do you want to be reminded?")
            engine.runAndWait()
            reminder_time = input("Reminder time: ")
            # Parse reminder time
            parsed_time = datetime.datetime.now()
            if "in" in reminder_time:
                time_delta = reminder_time.split(" ")[1]
                if "minute" in time_delta:
                    parsed_time += datetime.timedelta(minutes=int(time_delta[:-7]))
                elif "hour" in time_delta:
                    parsed_time += datetime.timedelta(hours=int(time_delta[:-5]))
            else:
                parsed_time = datetime.datetime.strptime(reminder_time, "%I:%M %p")
                if parsed_time < datetime.datetime.now():
                    parsed_time += datetime.timedelta(days=1)
            # Schedule reminder
            delay = (parsed_time - datetime.datetime.now()).total_seconds()
            timer = QtCore.QTimer()
            timer.singleShot(delay * 1000, lambda: remind(reminder_text))
            print(f"Reminder set for {parsed_time.strftime('%I:%M %p on %A, %B %d')}")
            engine.say(f"Reminder set for {parsed_time.strftime('%I:%M %p on %A, %B %d')}")
            engine.runAndWait()

    ui.submitButton.clicked.connect(button_click)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()