import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from datetime import datetime
from control import get_items_to_widget, get_count_save


class ResultsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Результаты")
        self.setGeometry(500, 50, 575, 562)
        font = QFont()
        font.setPointSize(12)
        main_widget = QWidget()
        main_widget.setObjectName("main_widget")
        vertical_layout = QVBoxLayout()
        vertical_layout.setObjectName("vertical_layout")
        self.table_results = QTableWidget(self)
        self.table_results.setMinimumSize(553, 350)
        self.table_results.setFont(font)
        self.table_results.setLayoutDirection(Qt.LeftToRight)
        self.table_results.setAutoFillBackground(False)
        self.table_results.setObjectName("table_results")
        self.table_results.setColumnCount(3)
        self.table_results.setHorizontalHeaderLabels(["Имя", "Дата", "Время"])
        vertical_layout.addWidget(self.table_results)
        grid_layout = QGridLayout()
        grid_layout.setObjectName("grid_layout")
        self.button_sort_1 = QPushButton("Сортировать по имени", self)
        self.button_sort_1.setMinimumSize(250, 40)
        self.button_sort_1.setMaximumSize(250, 40)
        self.button_sort_1.setFont(font)
        self.button_sort_1.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_sort_1.setObjectName("button_sort_1")
        self.button_sort_1.clicked.connect(self.click_sort_1)
        grid_layout.addWidget(self.button_sort_1, 0, 0)
        self.button_sort_2 = QPushButton("Сортировтаь по дате", self)
        self.button_sort_2.setMinimumSize(250, 40)
        self.button_sort_2.setMaximumSize(250, 40)
        self.button_sort_2.setFont(font)
        self.button_sort_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_sort_2.setObjectName("button_sort_2")
        self.button_sort_2.clicked.connect(self.click_sort_2)
        grid_layout.addWidget(self.button_sort_2, 1, 0)
        self.button_show = QPushButton("Показать", self)
        self.button_show.setMinimumSize(250, 40)
        self.button_show.setMaximumSize(250, 40)
        self.button_show.setFont(font)
        self.button_show.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_show.setObjectName("button_show")
        self.button_show.clicked.connect(self.click_show)
        grid_layout.addWidget(self.button_show, 2, 0)
        self.button_save = QPushButton("Сохранить", self)
        self.button_save.setMinimumSize(250, 40)
        self.button_save.setMaximumSize(250, 40)
        self.button_save.setFont(font)
        self.button_save.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_save.setObjectName("button_save")
        self.button_save.clicked.connect(self.click_save)
        grid_layout.addWidget(self.button_save, 3, 0)
        label_from = QLabel("От:", self)
        label_from.setMinimumSize(80, 40)
        label_from.setMaximumSize(80, 40)
        label_from.setFont(font)
        label_from.setObjectName("label_from")
        grid_layout.addWidget(label_from, 2, 1)
        label_to = QLabel("До:", self)
        label_to.setMinimumSize(80, 40)
        label_to.setMaximumSize(80, 40)
        label_to.setFont(font)
        label_to.setObjectName("label_to")
        grid_layout.addWidget(label_to, 3, 1)
        self.date_from = QDateEdit(self)
        self.date_from.setMinimumSize(150, 30)
        self.date_from.setMaximumSize(150, 30)
        self.date_from.setFont(font)
        self.date_from.setDate(QDate(2022, 6, 1))
        self.date_from.setMinimumDate(QDate(2022, 6, 1))
        self.date_from.setObjectName("date_from")
        grid_layout.addWidget(self.date_from, 2, 2)
        self.date_to = QDateEdit(self)
        self.date_to.setMinimumSize(150, 30)
        self.date_to.setMaximumSize(150, 30)
        self.date_to.setFont(font)
        self.date_to.setDate(QDate(2022, 6, 1))
        self.date_to.setMinimumDate(QDate(2022, 6, 1))
        self.date_to.setObjectName("date_to")
        grid_layout.addWidget(self.date_to, 3, 2)
        self.time_from = QTimeEdit(self)
        self.time_from.setMinimumSize(150, 30)
        self.time_from.setMaximumSize(150, 30)
        self.time_from.setFont(font)
        self.time_from.setObjectName("time_from")
        grid_layout.addWidget(self.time_from, 2, 3)
        self.time_to = QTimeEdit(self)
        self.time_to.setMinimumSize(150, 30)
        self.time_to.setMaximumSize(150, 30)
        self.time_to.setFont(font)
        self.time_to.setObjectName("time_to")
        grid_layout.addWidget(self.time_to, 3, 3)
        vertical_layout.addLayout(grid_layout)
        main_widget.setLayout(vertical_layout)
        self.setCentralWidget(main_widget)
        self.show_results()
        self.show()

    def show_results(self):
        items = get_items_to_widget()
        self.show_items(items)

    def click_sort_1(self):
        self.table_results.sortItems(0, Qt.AscendingOrder)

    def click_sort_2(self):
        self.table_results.sortItems(1, Qt.AscendingOrder)

    def click_show(self):
        items = get_items_to_widget()
        date_from = self.date_from.date().toPyDate()
        date_to = self.date_to.date().toPyDate()
        time_from = self.time_from.time().toPyTime()
        time_to = self.time_to.time().toPyTime()
        date_from_combine = datetime.combine(date_from, time_from)
        date_to_combine = datetime.combine(date_to, time_to)
        new_items = []
        for item in items:
            date_item = item["date"]
            time_item = item["time"]
            date_item_format = datetime.strptime(date_item + " " + time_item, "%Y-%m-%d %H:%M:%S")
            if (date_from_combine <= date_item_format) & (date_to_combine >= date_item_format):
                new_item = {"p_name": item["p_name"],
                            "date": item["date"],
                            "time": item["time"]}
                new_items.append(new_item)
        self.show_items(new_items)

    def show_items(self, items):
        self.table_results.clear()
        self.table_results.setRowCount(get_count_save())
        indx = 0
        for item in items:
            self.table_results.setItem(indx, 0, QTableWidgetItem(item["p_name"]))
            self.table_results.setItem(indx, 1, QTableWidgetItem(item["date"]))
            self.table_results.setItem(indx, 2, QTableWidgetItem(item["time"]))
            indx += 1

    def click_save(self):
        new_file = "resources/review_" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + ".txt"
        with open(new_file, "w") as file_write:
            for i in range(self.table_results.rowCount()):
                file_write.write("p_name: " + self.table_results.item(i, 0).text() +
                                 ", date: " + self.table_results.item(i, 1).text() +
                                 ", time: " + self.table_results.item(i, 2).text() + "\n")