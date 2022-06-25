import cv2
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from multiprocessing.pool import ThreadPool

from detection_and_recognition import find_faces_from_camera


class ThreadCamera(QThread):

    change_pixmap = pyqtSignal(QImage)
    return_results = pyqtSignal(list)

    def __init__(self, predict_model_path):
        super().__init__()
        self.running = True
        self.predict_model_path = predict_model_path

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.running = True
        num = 1
        while self.running:
            ret, frame = cap.read()
            if ret:
                if num % 100 == 0:
                    pool = ThreadPool(processes=4)
                    async_result = pool.apply_async(find_faces_from_camera, (frame, self.predict_model_path))
                    return_values = async_result.get()
                    self.return_results.emit(return_values)
                    pool.close()
                frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height = frame_color.shape[0]
                width = frame_color.shape[1]
                image = QImage(frame_color.data, width, height, QImage.Format_RGB888)
                self.change_pixmap.emit(image)
            num += 1
        cap.release()

    def stop(self):
        self.running = False