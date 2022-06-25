import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime

from window_fit_model import FitModelWindow
from detection_and_recognition import find_face
from control import set_items_from_widget


class PictureRecognitionWindow(QMainWindow):
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
        self.button_choose_picture = QPushButton("Выбрать изображение", self)
        self.button_choose_picture.setMinimumSize(250, 40)
        self.button_choose_picture.setMaximumSize(250, 40)
        self.button_choose_picture.setFont(font)
        self.button_choose_picture.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_choose_picture.setObjectName("button_choose_picture")
        self.button_choose_picture.clicked.connect(self.click_choose_picture)
        grid_small.addWidget(self.button_choose_picture, 0, 0)
        self.button_choose_model = QPushButton("Выбрать модель", self)
        self.button_choose_model.setMinimumSize(250, 40)
        self.button_choose_model.setMaximumSize(250, 40)
        self.button_choose_model.setFont(font)
        self.button_choose_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_choose_model.setObjectName("button_choose_model")
        self.button_choose_model.clicked.connect(self.click_choose_model)
        grid_small.addWidget(self.button_choose_model, 1, 0)
        self.button_new_model = QPushButton("Новая модель", self)
        self.button_new_model.setMinimumSize(250, 40)
        self.button_new_model.setMaximumSize(250, 40)
        self.button_new_model.setFont(font)
        self.button_new_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_new_model.setObjectName("button_new_model")
        self.button_new_model.clicked.connect(self.click_new_model)
        grid_small.addWidget(self.button_new_model, 2, 0)
        self.button_recognize = QPushButton("Распознать", self)
        self.button_recognize.setMinimumSize(250, 40)
        self.button_recognize.setMaximumSize(250, 40)
        self.button_recognize.setFont(font)
        self.button_recognize.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_recognize.setObjectName("button_recognize")
        self.button_recognize.clicked.connect(self.click_recognize)
        self.button_recognize.setEnabled(False)
        grid_small.addWidget(self.button_recognize, 3, 0)
        self.button_save = QPushButton("Сохранить результаты", self)
        self.button_save.setMinimumSize(250, 40)
        self.button_save.setMaximumSize(250, 40)
        self.button_save.setFont(font)
        self.button_save.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_save.setObjectName("button_save")
        self.button_save.clicked.connect(self.click_save)
        self.button_save.setEnabled(False)
        grid_small.addWidget(self.button_save, 4, 0)
        self.line_picture = QLineEdit(self)
        self.line_picture.setMinimumSize(489, 30)
        self.line_picture.setMaximumSize(489, 30)
        self.line_picture.setFont(font)
        self.line_picture.setObjectName("line_picture")
        grid_small.addWidget(self.line_picture, 0, 2)
        self.line_model = QLineEdit(self)
        self.line_model.setMinimumSize(489, 30)
        self.line_model.setMaximumSize(489, 30)
        self.line_model.setFont(font)
        self.line_model.setObjectName("line_model")
        grid_small.addWidget(self.line_model, 1, 2)
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

    def click_choose_picture(self):
        self.list_faces.clear()
        file_path = QFileDialog.getOpenFileName(self, "Open file", "./", "*.jpg *.png")[0]
        pixmap = QPixmap(file_path)
        if pixmap.width() > pixmap.height():
            pixmap2 = pixmap.scaledToWidth(650)
        else:
            pixmap2 = pixmap.scaledToHeight(650)
        self.label_show.setPixmap(pixmap2)
        self.line_picture.setText(file_path)
        if self.line_picture.text().strip():
            if self.line_model.text().strip():
                self.button_recognize.setEnabled(True)
        else:
            self.button_recognize.setEnabled(False)

    def click_choose_model(self):
        model_path = QFileDialog.getOpenFileName(self, "Open file", "./resources", "*.hdf5")[0]
        self.line_model.setText(model_path)
        if self.line_model.text().strip():
            if self.line_picture.text().strip():
                self.button_recognize.setEnabled(True)
        else:
            self.button_recognize.setEnabled(False)

    def click_recognize(self):
        self.list_faces.clear()
        results_names = find_face(self.line_picture.text(), self.line_model.text())
        for name in results_names:
            self.list_faces.addItem(name)
        self.button_save.setEnabled(True)

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