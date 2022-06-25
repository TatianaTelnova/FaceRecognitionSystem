import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from window_picture_recognition import PictureRecognitionWindow
from window_camera_recognition import CameraRecognitionWindow
from window_models import ModelsWindow
from window_results import ResultsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Система распознавания лиц")
        self.setGeometry(300, 200, 510, 100)
        font = QFont()
        font.setPointSize(12)
        grid_layout = QGridLayout()
        self.button_picture = QPushButton("Распознавание на изображении", self)
        self.button_picture.setMinimumSize(350, 40)
        self.button_picture.setFont(font)
        self.button_picture.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_picture.setObjectName("button_picture")
        self.button_picture.clicked.connect(self.click_picture)
        grid_layout.addWidget(self.button_picture, 0, 0)
        self.button_camera = QPushButton("Распознавание в видеопотоке", self)
        self.button_camera.setMinimumSize(350, 40)
        self.button_camera.setFont(font)
        self.button_camera.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_camera.setObjectName("button_camera")
        self.button_camera.clicked.connect(self.click_camera)
        grid_layout.addWidget(self.button_camera, 1, 0)
        self.button_models = QPushButton("Модели распознавания", self)
        self.button_models.setMinimumSize(350, 40)
        self.button_models.setFont(font)
        self.button_models.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_models.setObjectName("button_models")
        self.button_models.clicked.connect(self.click_models)
        grid_layout.addWidget(self.button_models, 0, 1)
        self.button_results = QPushButton("Результаты", self)
        self.button_results.setMinimumSize(350, 40)
        self.button_results.setFont(font)
        self.button_results.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_results.setObjectName("button_results")
        self.button_results.clicked.connect(self.click_results)
        grid_layout.addWidget(self.button_results, 1, 1)
        main_widget = QWidget()
        main_widget.setLayout(grid_layout)
        self.setCentralWidget(main_widget)
        self.show()

    def click_picture(self):
        self.pic_win = PictureRecognitionWindow()
        self.close()

    def click_camera(self):
        self.cam_win = CameraRecognitionWindow()
        self.close()

    def click_models(self):
        self.mod_win = ModelsWindow()
        self.close()

    def click_results(self):
        self.res_win = ResultsWindow()
        self.close()