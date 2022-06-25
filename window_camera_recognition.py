import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime

from window_fit_model import FitModelWindow
from class_camera import ThreadCamera
from control import set_items_from_widget


class CameraRecognitionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Распознавание лиц")
        self.setGeometry(500, 50, 983, 911)
        font = QFont()
        font.setPointSize(12)
        main_widget = QWidget()
        main_widget.setObjectName("main_widget")
        grid_big = QGridLayout()
        grid_big.setObjectName("grid_big")
        grid_small = QGridLayout()
        grid_small.setObjectName("grid_small")
        self.button_choose_model = QPushButton("Выбрать модель", self)
        self.button_choose_model.setMinimumSize(250, 40)
        self.button_choose_model.setMaximumSize(250, 40)
        self.button_choose_model.setFont(font)
        self.button_choose_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_choose_model.setObjectName("button_choose_model")
        self.button_choose_model.clicked.connect(self.click_choose_model)
        grid_small.addWidget(self.button_choose_model, 0, 0)
        self.button_start = QPushButton("Начать", self)
        self.button_start.setMinimumSize(250, 40)
        self.button_start.setMaximumSize(250, 40)
        self.button_start.setFont(font)
        self.button_start.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start.setObjectName("button_start")
        self.button_start.clicked.connect(self.click_start_camera)
        self.button_start.setEnabled(False)
        grid_small.addWidget(self.button_start, 1, 0)
        self.button_stop = QPushButton("Остановить", self)
        self.button_stop.setMinimumSize(250, 40)
        self.button_stop.setMaximumSize(250, 40)
        self.button_stop.setFont(font)
        self.button_stop.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_stop.setObjectName("button_stop")
        self.button_stop.setEnabled(False)
        self.button_stop.clicked.connect(self.click_stop_camera)
        grid_small.addWidget(self.button_stop, 2, 0)
        self.button_new_model = QPushButton("Новая модель", self)
        self.button_new_model.setMinimumSize(250, 40)
        self.button_new_model.setMaximumSize(250, 40)
        self.button_new_model.setFont(font)
        self.button_new_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_new_model.setObjectName("button_new_model")
        self.button_new_model.clicked.connect(self.click_new_model)
        grid_small.addWidget(self.button_new_model, 3, 0)
        self.button_save = QPushButton("Сохранить результаты", self)
        self.button_save.setMinimumSize(250, 40)
        self.button_save.setMaximumSize(250, 40)
        self.button_save.setFont(font)
        self.button_save.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_save.setObjectName("button_save")
        self.button_save.clicked.connect(self.click_save)
        self.button_save.setEnabled(False)
        grid_small.addWidget(self.button_save, 4, 0)
        self.line_model = QLineEdit(self)
        self.line_model.setMinimumSize(489, 30)
        self.line_model.setMaximumSize(489, 30)
        self.line_model.setFont(font)
        self.line_model.setObjectName("line_model")
        grid_small.addWidget(self.line_model, 0, 1)
        grid_big.addLayout(grid_small, 1, 0)
        self.label_show = QLabel(self)
        self.label_show.setMinimumSize(650, 650)
        self.label_show.setMaximumSize(650, 650)
        self.label_show.setAlignment(Qt.AlignCenter)
        self.label_show.setObjectName("label_show")
        grid_big.addWidget(self.label_show, 0, 0)
        vertical_layout = QVBoxLayout()
        vertical_layout.setObjectName("vertical_layout")
        label_results = QLabel("Результаты", self)
        label_results.setMinimumSize(300, 24)
        label_results.setMaximumSize(1000, 24)
        label_results.setFont(font)
        label_results.setAlignment(Qt.AlignCenter)
        label_results.setObjectName("label_results")
        vertical_layout.addWidget(label_results)
        self.list_faces = QListWidget(self)
        self.list_faces.setMinimumSize(300, 617)
        self.list_faces.setMaximumSize(1000, 1000)
        self.list_faces.setFont(font)
        self.list_faces.setObjectName("list_faces")
        vertical_layout.addWidget(self.list_faces)
        grid_big.addLayout(vertical_layout, 0, 1)
        main_widget.setLayout(grid_big)
        self.setCentralWidget(main_widget)
        self.show()

    def click_choose_model(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "./resources", "*.hdf5")[0]
        self.line_model.setText(fname)
        if self.line_model.text().strip():
            self.button_start.setEnabled(True)
        else:
            self.button_start.setEnabled(False)
            self.button_stop.setEnabled(False)

    def click_new_model(self):
        self.fit_model_win = FitModelWindow()

    def click_save(self):
        date_time = datetime.now()
        date = str(date_time.date())
        time = str(date_time.time().strftime("%H:%M:%S"))
        items_save = []
        for i in range(self.list_faces.count()):
            item = {"p_name": self.list_faces.item(i).text(),
                    "date": date,
                    "time": time}
            items_save.append(item)
        set_items_from_widget(self.line_model.text(), items_save)
        self.button_save.setEnabled(False)

    def click_start_camera(self):
        self.thread = ThreadCamera(self.line_model.text())
        self.thread.change_pixmap.connect(self.show_new_frame)
        self.thread.return_results.connect(self.show_results)
        self.thread.start()
        self.button_stop.setEnabled(True)

    def click_stop_camera(self):
        self.thread.running = False
        self.button_stop.setEnabled(False)

    def show_new_frame(self, image):
        self.label_show.setPixmap(QPixmap.fromImage(image))

    def show_results(self, items):
        if len(items) > 0:
            for item in items:
                self.list_faces.addItem(item)
            self.button_save.setEnabled(True)