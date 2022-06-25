from keras.models import load_model
import tensorflow as tf
import numpy as np
import os

from control import get_count_all, get_person_to_widget


def limit(folders):
    return 1 / (2 * folders) + 0.4


def predict_name(img, predict_model_path):
    collection_faces = os.path.splitext(os.path.basename(predict_model_path))[0]
    lmt = limit(get_count_all(collection_faces))
    model = load_model(predict_model_path)
    input_arr = tf.keras.preprocessing.image.img_to_array(img)
    input_arr = np.array([input_arr])
    predict = model.predict(input_arr)
    if np.max(predict) >= lmt:
        p_class = int(np.argmax(predict))
        person_name = get_person_to_widget(collection_faces, p_class)
        return person_name
    else:
        return "unknown person"