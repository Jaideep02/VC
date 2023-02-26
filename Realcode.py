import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QLinearGradient, QColor, QPainter
from PyQt5 import QtCore

class GradientWindow(QWidget):
    def __init__(self):
        super().__init__()

        # get screen dimensions
        screen = QApplication.primaryScreen()
        screen_size = screen.size()

        # set window dimensions and position
        window_width = screen_size.width() // 2
        window_height = screen_size.height() // 2
        window_x = (screen_size.width() - window_width) // 2
        window_y = (screen_size.height() - window_height) // 2
        self.setGeometry(window_x, window_y, 1000, 700)

        self.setWindowTitle("Gradient Window")

        # create a button and a label
        self.button = QPushButton("Press me", self)
        self.label = QLabel("", self)

        # create a vertical layout and add the label
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        # create a grid layout and add the button to the center
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # set button dimensions and add it to the grid layout
        self.button.setMinimumSize(100, 50)
        grid_layout.addWidget(self.button, 0, 0, 1, 1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        # connect the button clicked signal to the on_button_clicked method
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.label.setText("I'm pressed")

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(1, 43, 77))
        gradient.setColorAt(1.0, QColor(0, 0, 0))
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GradientWindow()
    window.show()
    sys.exit(app.exec_())
