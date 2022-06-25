from keras.layers import Input, Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.applications.vgg19 import VGG19
from keras.applications.vgg16 import VGG16
from keras.applications.resnet import ResNet50
from keras.applications.resnet import ResNet152
from keras.applications.resnet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np


def get_data(path_training):
    batch_size = 1
    target_size = (100, 100)
    gen = ImageDataGenerator(
        rescale=1. / 255,
        preprocessing_function=preprocess_input,
        validation_split=0.5
    )
    train_data = gen.flow_from_directory(
        path_training,
        target_size=target_size,
        batch_size=batch_size,
        subset="training"
    )
    valid_data = gen.flow_from_directory(
        path_training,
        target_size=target_size,
        batch_size=batch_size,
        subset="validation"
    )
    return train_data, valid_data


def cnn_models_info(path_training):
    train_data, valid_data = get_data(path_training)
    labels = {}
    for k, v in train_data.class_indices.items():
        labels[v] = k
    input_size = (100, 100, 3)
    vgg16 = VGG16(include_top=False, weights="imagenet", input_shape=input_size)
    vgg19 = VGG19(include_top=False, weights="imagenet", input_shape=input_size)
    resnet50 = ResNet50(include_top=False, weights="imagenet", input_shape=input_size)
    resnet152 = ResNet152(include_top=False, weights="imagenet", input_shape=input_size)
    vgg16.trainable = False
    vgg19.trainable = False
    resnet50.trainable = False
    resnet152.trainable = False
    folders = train_data.num_classes
    inputs = Input(shape=input_size)
    x = vgg16(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    outputs = Dense(folders, activation="softmax")(x)
    model_16 = Model(inputs, outputs)
    x = vgg19(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    outputs = Dense(folders, activation="softmax")(x)
    model_19 = Model(inputs, outputs)
    x = resnet50(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    outputs = Dense(folders, activation="softmax")(x)
    model_50 = Model(inputs, outputs)
    x = resnet152(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    outputs = Dense(folders, activation="softmax")(x)
    model_152 = Model(inputs, outputs)
    model_16.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
    model_19.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
    model_50.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
    model_152.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
    batch_size = 1
    epochs = 25
    model_history_16 = model_16.fit(
        train_data,
        validation_data=valid_data,
        epochs=epochs,
        steps_per_epoch=train_data.samples // batch_size,
        validation_steps=valid_data.samples // batch_size,
    )
    model_history_19 = model_19.fit(
        train_data,
        validation_data=valid_data,
        epochs=epochs,
        steps_per_epoch=train_data.samples // batch_size,
        validation_steps=valid_data.samples // batch_size,
    )
    model_history_50 = model_50.fit(
        train_data,
        validation_data=valid_data,
        epochs=epochs,
        steps_per_epoch=train_data.samples // batch_size,
        validation_steps=valid_data.samples // batch_size,
    )
    model_history_152 = model_152.fit(
        train_data,
        validation_data=valid_data,
        epochs=epochs,
        steps_per_epoch=train_data.samples // batch_size,
        validation_steps=valid_data.samples // batch_size,
    )
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.plot(model_history_16.history["loss"], "r", label="VGG16 train", linestyle="--")
    ax.plot(model_history_16.history["val_loss"], "r", label="VGG16 val", linestyle="-")
    ax.plot(model_history_19.history["loss"], "b", label="VGG19 train", linestyle="--")
    ax.plot(model_history_19.history["val_loss"], "b", label="VGG19 val", linestyle="-")
    ax.plot(model_history_50.history["loss"], "g", label="ResNet50 train", linestyle="--")
    ax.plot(model_history_50.history["val_loss"], "g", label="ResNet50 val", linestyle="-")
    ax.plot(model_history_152.history["loss"], "k", label="ResNet152 train", linestyle="--")
    ax.plot(model_history_152.history["val_loss"], "k", label="ResNet152 val", linestyle="-")
    ax.set_xlabel(r"Epoch", fontsize=14)
    ax.set_ylabel(r"Loss", fontsize=14)
    ax.legend()
    ax.tick_params(labelsize=14)
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.plot(model_history_16.history["accuracy"], "r", label="VGG16 train", linestyle="--")
    ax.plot(model_history_16.history["val_accuracy"], "r", label="VGG16 val", linestyle="-")
    ax.plot(model_history_19.history["accuracy"], "b", label="VGG19 train", linestyle="--")
    ax.plot(model_history_19.history["val_accuracy"], "b", label="VGG19 val", linestyle="-")
    ax.plot(model_history_50.history["accuracy"], "g", label="ResNet50 train", linestyle="--")
    ax.plot(model_history_50.history["val_accuracy"], "g", label="ResNet50 val", linestyle="-")
    ax.plot(model_history_152.history["accuracy"], "k", label="ResNet152 train", linestyle="--")
    ax.plot(model_history_152.history["val_accuracy"], "k", label="ResNet152 val", linestyle="-")
    ax.set_xlabel(r"Epoch", fontsize=14)
    ax.set_ylabel(r"Accuracy", fontsize=14)
    ax.legend()
    ax.tick_params(labelsize=14)