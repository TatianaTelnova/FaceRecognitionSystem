import cv2
import joblib
import numpy as np
from statistics import mean

from class_hog import HogProcessing


def check_area(tuple_list, area):
    for i in range(len(tuple_list)):
        tuple_sub = tuple(map(lambda x, y: x - y, tuple_list[i], area))
        if (tuple_sub[0] <= 0) & (tuple_sub[1] <= 0) & (tuple_sub[2] >= 0) & (tuple_sub[3] >= 0):
            return tuple_list[i][2]
    return 0


def areas(tuple_list, min_cnt):
    tuple_map = []
    tuple_max = []
    for i in range(len(tuple_list)):
        if len(tuple_max) > 0:
            b = False
            diff = 0.25 * (tuple_list[i][2] - tuple_list[i][0])
            for j in range(len(tuple_max)):
                tuple_new = tuple(map(lambda x, y: x - y, tuple_max[j], tuple_list[i]))
                if all(map(lambda x: abs(x) < diff, tuple_new)):
                    tuple_max[j][2] = tuple_list[i][2]
                    tuple_max[j][3] = tuple_list[i][3]
                    tuple_map[j].append(tuple_list[i])
                    b = True
                    break
            if not b:
                tuple_max.append(list(tuple_list[i]))
                tuple_map.append([tuple_list[i]])
        else:
            tuple_max.append(list(tuple_list[i]))
            tuple_map.append([tuple_list[i]])
    tuple_areas = []
    for t_map in tuple_map:
        if len(t_map) >= min_cnt:
            tuple_areas.append(tuple(int(mean(tll)) for tll in [tuple(tl) for tl in zip(*t_map)]))
    return tuple_areas


def find_faces_areas(img, min_step=24, check_sizes=(4, 5), area_sizes=(80, 80), classifier="resources/classifier.joblib"):
    # размер окна
    if img.shape[1] / check_sizes[0] < img.shape[0] / check_sizes[1]:
        win_width = round(img.shape[1])
        win_height = round(img.shape[1] / check_sizes[0] * check_sizes[1])
    else:
        win_height = round(img.shape[0])
        win_width = round(img.shape[0] / check_sizes[1] * check_sizes[0])
    find = 0
    i = 0
    tuple_list = []
    while i < 6:
        reduction = round(1 - i / 10, 3)
        width = int(win_width * reduction)
        height = int(win_height * reduction)
        step = int(0.05 * width) if width > min_step * 20 else min_step
        y = 0
        while y < img.shape[0] - height + 1:
            x = 0
            while x < img.shape[1] - width + 1:
                ca = check_area(tuple_list, (x, y, x + width, y + height))
                if ca == 0:
                    crop_img = img[y:y + height, x:x + width]
                    resize_crop_img = cv2.resize(crop_img, (area_sizes[0]+2, area_sizes[1]+2), interpolation=cv2.INTER_CUBIC)
                    features = [np.round(HogProcessing(resize_crop_img).hog_features, 3)]
                    find_faces_classifier = joblib.load(classifier)
                    ans = find_faces_classifier.predict(features)
                    if ans == 1:
                        find += 1
                        tuple_list.append((x, y, x + width, y + height))
                    x += step
                else:
                    x = ca
            y += step
        i += 1

    tuple_areas_c = areas(tuple_list, 2)
    while True:
        tuple_areas_n = areas(tuple_areas_c, 1)
        if tuple_areas_c == tuple_areas_n:
            break
        tuple_areas_c = tuple_areas_n
    return tuple_areas_c