import os
from keras.layers import Input, Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.applications.vgg19 import VGG19
from keras.applications.vgg16 import preprocess_input
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

from control import set_items_from_fit


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


def limit(folders):
    return 1 / (2 * folders) + 0.4


def check_folder():
    if not os.path.exists("resources/checkpoint_files"):
        os.mkdir("resources/checkpoint_files")


def delete_checkpoints(path_checkpoint):
    os.remove("resources/checkpoint_files/" + path_checkpoint)
    os.remove("resources/checkpoint_files/second_" + path_checkpoint)


def predict_model_fit(path_training, path_checkpoint, saving, path_saving, epochs):
    check_folder()
    train_data, valid_data = get_data(path_training)
    collection_faces = path_saving.split(".")[0]
    people_all = []
    for k, v in train_data.class_indices.items():
        people = {"p_class": v,
                  "p_name": k}
        people_all.append(people)
    set_items_from_fit(collection_faces, people_all)
    input_size = (100, 100, 3)
    vgg19 = VGG19(include_top=False, weights="imagenet", input_shape=input_size)
    vgg19.trainable = False
    folders = train_data.num_classes
    inputs = Input(shape=input_size)
    x = vgg19(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    outputs = Dense(folders, activation="softmax")(x)
    model_19 = Model(inputs, outputs)
    model_19.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
    batch_size = 1
    delete_checkpoints(path_checkpoint)
    mc = ModelCheckpoint(
        filepath="resources/checkpoint_files/" + path_checkpoint,
        save_weights_only=True,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True
    )
    model_19.fit(
        train_data,
        validation_data=valid_data,
        epochs=epochs,
        steps_per_epoch=train_data.samples // batch_size,
        validation_steps=valid_data.samples // batch_size,
        callbacks=mc
    )
    model_19.load_weights("resources/checkpoint_files/" + path_checkpoint)
    vgg19.trainable = True
    model_19.compile(optimizer=Adam(1e-7), loss="categorical_crossentropy", metrics=["accuracy"])
    checkpoint_filepath_2 = "second_" + path_checkpoint
    mc2 = ModelCheckpoint(
        filepath="resources/checkpoint_files/" + checkpoint_filepath_2,
        save_weights_only=True,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True
    )
    model_19.fit(
        train_data,
        validation_data=valid_data,
        epochs=5,
        steps_per_epoch=train_data.samples // batch_size,
        validation_steps=valid_data.samples // batch_size,
        callbacks=mc2
    )
    model_19.load_weights("resources/checkpoint_files/" + checkpoint_filepath_2)
    if saving:
        model_19.save("resources/" + path_saving)