import os
import numpy as np


class HogProcessing(object):
    """
    HogProcessing класс определяет форму объекта на изображении с помощью гистограмм направленных градиентов
    """

    def __init__(self, image, cell_size=8):
        self.num = 9
        self.cell_size = cell_size
        self.cell_height = image.shape[0] // self.cell_size
        self.cell_width = image.shape[1] // self.cell_size
        height = image.shape[0]
        width = image.shape[1]
        grad_x = image[1:height - 1, 2:width] - image[1:height - 1, :width - 2]
        grad_y = image[2:height, 1:width - 1] - image[:height - 2, 1:width - 1]
        angle = np.arctan(np.divide(grad_y, grad_x, out=np.float16(np.zeros_like(grad_y)), where=grad_x != 0))
        # угол в радианах от 0 до п
        angle[angle < 0] = angle[angle < 0] + np.pi
        # угол в градусах от 0 до 180
        angle = np.uint8(angle * 180 / 3.14)
        magnitude = np.sqrt(np.power(grad_x, 2) + np.power(grad_y, 2))
        # разделение на ячейки
        self.angle_cell = np.uint8(self.__get_cells(angle))
        self.magnitude_cell = self.__get_cells(magnitude)
        # вычисление гистограмм направленных градиентов
        self.hog_cells = self.__get_hog_for_cells()
        self.hog_features = self.__get_hog_array()

    # делим на ячейки
    def __get_cells(self, data):
        cell = np.zeros(shape=(self.cell_height, self.cell_width, self.cell_size, self.cell_size))
        data_i = np.split(data, self.cell_height, axis=0)
        for i in range(self.cell_height):
            data_j = np.split(data_i[i], self.cell_width, axis=1)
            for j in range(self.cell_width):
                cell[i][j] = data_j[j]
        return cell

    # получаем hog для каждой ячейки
    def __get_hog_for_cells(self):
        cells = np.zeros(shape=(self.cell_height, self.cell_width, self.num))
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell = np.zeros(self.num)  # строка из 9 элементов
                magn_list = self.magnitude_cell[i, j].flatten()
                ang_list = self.angle_cell[i, j].flatten()
                ang_list = np.int8(ang_list / (180 / self.num))  # 0-9, целое число
                ang_list[ang_list >= self.num] = 0
                for m in range(len(ang_list)):
                    cell[ang_list[m]] += magn_list[m]
                cells[i][j] = cell
        return cells

    # массив-строка с признаками hog
    def __get_hog_array(self):
        feature = np.array([])
        for i in range(self.cell_height - 1):
            for j in range(self.cell_width - 1):
                a = np.array(self.hog_cells[i, j])
                b = np.array(self.hog_cells[i, j + 1])
                c = np.array(self.hog_cells[i + 1, j])
                d = np.array(self.hog_cells[i + 1, j + 1])
                tmp = np.append(a, [b, c, d])
                tmp = np.divide(tmp, np.mean(tmp), out=np.float16(np.zeros_like(tmp)), where=np.mean(tmp) != 0)
                feature = np.append(feature, tmp)
        return np.round(feature, 2)

    # матрица яркости пикселей
    def draw_hog_image(self):
        image = np.zeros(shape=(self.cell_height * self.cell_size, self.cell_width * self.cell_size))
        # 9 частей
        # 0-20, 20-40, 40-60, ...
        angle_unit = 180 // self.num
        cell_center = self.cell_size / 2
        max_mag = np.array(self.hog_cells).max()
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell_grad = self.hog_cells[i][j]
                cell_grad /= max_mag
                angle = 0
                angle_gap = angle_unit
                for magnitude in cell_grad:
                    angle_radian = np.radians(angle)
                    x_c = j * self.cell_size + cell_center
                    y_c = i * self.cell_size + cell_center
                    x1 = int(x_c + magnitude * cell_center * np.cos(angle_radian))
                    y1 = int(y_c - magnitude * cell_center * np.sin(angle_radian))
                    x2 = int(x_c - magnitude * cell_center * np.cos(angle_radian))
                    y2 = int(y_c + magnitude * cell_center * np.sin(angle_radian))
                    image = self.__draw_line(image, (x1, y1), (x2, y2), int(255 * np.sqrt(magnitude)))
                    angle += angle_gap
        return image

    @staticmethod
    def __draw_line(img, first_c, second_c, color):
        a = (first_c[1] - second_c[1]) / (first_c[0] - second_c[0]) if (first_c[0] - second_c[0]) != 0 else 0
        b = first_c[1] - a * first_c[0]
        x_coordinates = (first_c[0], second_c[0]) if first_c[0] < second_c[0] else (second_c[0], first_c[0])
        y_coordinates = (first_c[1], second_c[1]) if first_c[1] < second_c[1] else (second_c[1], first_c[1])
        for i in range(y_coordinates[0], y_coordinates[1] + 1):
            for j in range(x_coordinates[0], x_coordinates[1] + 1):
                if (i + 1 >= round(a * j + b)) & (i - 1 <= round(a * j + b)) & (img[i, j] < color):
                    img[i, j] = color
        return img