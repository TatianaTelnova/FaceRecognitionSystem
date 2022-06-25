import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from fit_model import predict_model_fit


class FitModelWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Новая модель")
        self.resize(844, 150)
        font = QFont()
        font.setPointSize(12)
        main_widget = QWidget()
        main_widget.setObjectName("main_widget")
        grid_layout = QGridLayout()
        grid_layout.setObjectName("grid_layout")
        self.button_choose = QPushButton("Выбрать папку", self)
        self.button_choose.setMinimumSize(250, 40)
        self.button_choose.setMaximumSize(250, 40)
        self.button_choose.setFont(font)
        self.button_choose.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_choose.setObjectName("button_choose")
        self.button_choose.clicked.connect(self.click_choose)
        grid_layout.addWidget(self.button_choose, 0, 2)
        self.button_fit = QPushButton("Создать", self)
        self.button_fit.setMinimumSize(250, 40)
        self.button_fit.setMaximumSize(250, 40)
        self.button_fit.setFont(font)
        self.button_fit.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_fit.setObjectName("button_fit")
        self.button_fit.clicked.connect(self.click_fit)
        self.button_fit.setEnabled(False)
        grid_layout.addWidget(self.button_fit, 1, 2)
        self.button_ok = QPushButton("Действие завершено", self)
        self.button_ok.setMinimumSize(250, 40)
        self.button_ok.setMaximumSize(250, 40)
        self.button_ok.setFont(font)
        self.button_ok.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_ok.setObjectName("button_ok")
        self.button_ok.clicked.connect(self.click_ok)
        self.button_ok.setEnabled(False)
        grid_layout.addWidget(self.button_ok, 2, 2)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout")
        label_folder = QLabel("Папка:", self)
        label_folder.setMinimumSize(150, 30)
        label_folder.setMaximumSize(150, 30)
        label_folder.setFont(font)
        label_folder.setObjectName("label_folder")
        grid_layout.addWidget(label_folder, 0, 0)
        self.line_folder = QLineEdit(self)
        self.line_folder.setMinimumSize(400, 30)
        self.line_folder.setMaximumSize(1000, 30)
        self.line_folder.setFont(font)
        self.line_folder.setInputMask("")
        self.line_folder.setText("")
        self.line_folder.setObjectName("line_folder")
        grid_layout.addWidget(self.line_folder, 0, 1)
        label_save = QLabel("Сохранить как:", self)
        label_save.setMinimumSize(150, 30)
        label_save.setMaximumSize(150, 30)
        label_save.setFont(font)
        label_save.setObjectName("label_save")
        grid_layout.addWidget(label_save, 1, 0)
        self.line_save = QLineEdit(self)
        self.line_save.setMinimumSize(400, 30)
        self.line_save.setMaximumSize(1000, 30)
        self.line_save.setFont(font)
        self.line_save.setInputMask("")
        self.line_save.setText("")
        self.line_save.setObjectName("line_save")
        grid_layout.addWidget(self.line_save, 1, 1)
        main_widget.setLayout(grid_layout)
        self.setCentralWidget(main_widget)
        self.show()

    def click_choose(self):
        fname = QFileDialog.getExistingDirectory(self, "Open file", "/home")
        self.line_folder.setText(fname)
        self.button_fit.setEnabled(True)

    def click_fit(self):
        folder_training = self.line_folder.text()
        save_model_name = self.line_save.text()
        if save_model_name.find(".") == -1:
            save_model_name += ".hdf5"
        elif save_model_name.split(".")[-1] != "hdf5":
            save_model_name += ".hdf5"
        if not save_model_name.strip():
            save_model_name = "untitled.hdf5"
        predict_model_fit(folder_training, "model_checkpoint.hdf5", True, save_model_name, 25)
        self.button_ok.setEnabled(True)

    def click_ok(self):
        self.close()