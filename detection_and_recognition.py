import cv2
import numpy as np

from face_detection import find_faces_areas
from face_recognition import predict_name


def find_face(img_path, predict_model_path):
    # цветное с произвольным размером
    img_color = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    prop = img_color.shape[1] / img_color.shape[0]
    img_height = 650
    img_width = int(650 * prop)
    # цветное с размером в (650, 650)
    img_resize = cv2.resize(img_color, (img_width, img_height), interpolation=cv2.INTER_CUBIC)
    tuple_names = find_faces_from_camera(img_resize, predict_model_path)
    return tuple_names


def find_faces_from_camera(img, predict_model_path):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tuple_faces = find_faces_areas(img_gray)
    tuple_names = []
    for t_faces in tuple_faces:
        crop_img = img[t_faces[1]:t_faces[3], t_faces[0]:t_faces[2]]
        resize_crop_img = cv2.resize(crop_img, (100, 100), interpolation=cv2.INTER_CUBIC)
        resize_crop_img = resize_crop_img[..., ::-1]
        name = predict_name(resize_crop_img, predict_model_path)
        tuple_names.append(name)
    return tuple_names