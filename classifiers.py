import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn import svm


def classifier_training_info(classifier_training_file, saving, classifier_filename):
    data = pd.read_csv(classifier_training_file, delimiter=",", header=None)
    # все, кроме последнего столбца
    x = data.iloc[:, :- 1]
    # только последний столбец
    y = data.iloc[:, -1]

    # разделение данных на обучающую и тестовую выборки
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10, stratify=y)
    print("Training size:", y_train.shape)
    print("Number of items by class:")
    print(y_train.value_counts())

    # разделение данных на обучающую и тестовую выборки
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, train_size=0.6, random_state=10, stratify=y_test)
    print("Test size:", y_test.shape)
    print("Number of items by class:")
    print(y_test.value_counts())
    print("Validation size", y_val.shape)
    print("Number of items by class:")
    print(y_val.value_counts())

    # классификатор №2
    svc_model_2 = svm.SVC(kernel="rbf", gamma="auto", class_weight="balanced")
    svc_model_2.fit(x_train, y_train)
    y_test_svc_2 = svc_model_2.predict(x_test)
    y_val_svc_2 = svc_model_2.predict(x_val)
    f1_test_svc_2 = f1_score(y_true=y_test, y_pred=y_test_svc_2)
    f1_val_svc_2 = f1_score(y_true=y_val, y_pred=y_val_svc_2)
    print("Score of SVM:", f1_test_svc_2)
    print("Score of SVM on validation data:", f1_val_svc_2)
    target_names = ["not faces", "faces"]
    cm = confusion_matrix(y_val, y_val_svc_2, labels=svc_model_2.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target_names)
    disp.plot()
    plt.show()
    print(classification_report(y_val, y_val_svc_2, target_names=target_names))

    if saving:
        joblib.dump(svc_model_2, classifier_filename)
