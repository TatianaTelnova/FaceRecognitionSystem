import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os

from window_fit_model import FitModelWindow
from control import delete_from_widget


class ModelsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Модели")
        self.setGeometry(500, 50, 488, 221)
        font = QFont()
        font.setPointSize(12)
        main_widget = QWidget()
        main_widget.setObjectName("main_widget")
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setObjectName("vertical_layout")
        self.list_models = QListWidget(self)
        self.list_models.setMinimumSize(466, 150)
        self.list_models.setFont(font)
        self.list_models.setObjectName("list_models")
        vertical_layout.addWidget(self.list_models)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout")
        self.button_reload = QPushButton("Обновить", self)
        self.button_reload.setMinimumSize(250, 40)
        self.button_reload.setMaximumSize(250, 40)
        self.button_reload.setFont(font)
        self.button_reload.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_reload.setObjectName("button_reload")
        self.button_reload.clicked.connect(self.show_models)
        horizontal_layout.addWidget(self.button_reload)
        self.button_new = QPushButton("Новая модель", self)
        self.button_new.setMinimumSize(250, 40)
        self.button_new.setMaximumSize(250, 40)
        self.button_new.setFont(font)
        self.button_new.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_new.setObjectName("button_new")
        self.button_new.clicked.connect(self.click_new)
        horizontal_layout.addWidget(self.button_new)
        self.button_delete = QPushButton("Удалить", self)
        self.button_delete.setMinimumSize(250, 40)
        self.button_delete.setMaximumSize(250, 40)
        self.button_delete.setFont(font)
        self.button_delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_delete.setObjectName("button_delete")
        self.button_delete.clicked.connect(self.click_delete)
        self.button_delete.setEnabled(False)
        horizontal_layout.addWidget(self.button_delete)
        vertical_layout.addLayout(horizontal_layout)
        main_widget.setLayout(vertical_layout)
        self.setCentralWidget(main_widget)
        self.show_models()
        self.show()

    def show_models(self):
        self.list_models.clear()
        path = "resources"
        for files in os.listdir(path):
            if files.split(".")[-1] == "hdf5":
                self.list_models.addItem(files)
        if self.list_models.count() > 0:
            self.button_delete.setEnabled(True)

    def click_delete(self):
        delete_file = self.list_models.selectedItems()[0].text()
        delete_from_widget(delete_file)
        self.show_models()
        if self.list_models.count() == 0:
            self.button_delete.setEnabled(False)

    def click_new(self):
        self.fit_win = FitModelWindow()