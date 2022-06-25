import pandas as pd
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, NeighborhoodComponentsAnalysis


def classifiers_info(classifier_training_file):
    data = pd.read_csv(classifier_training_file, delimiter=",", header=None)
    # все, кроме последнего столбца
    x = data.iloc[:, :- 1]
    # только последний столбец
    y = data.iloc[:, -1]

    # разделение данных на обучающую и тестовую выборки
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10, stratify=y)
    print("Размер обучающей выборки:", y_train.shape)
    print("Количество объектов по классам:")
    print(y_train.value_counts())

    # разделение данных на тестовую и контрольную выборки
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, train_size=0.6, random_state=10, stratify=y_test)
    print("Размер тестовой выборки:", y_test.shape)
    print("Количество объектов объектов по классам:")
    print(y_test.value_counts())
    print("Размер валидационной выборки:", y_val.shape)
    print("Количество объектов по классам:")
    print(y_val.value_counts())

    # классификатор 1
    svc_model = svm.SVC()
    svc_model.fit(x_train, y_train)
    y_test_svc = svc_model.predict(x_test)
    print("Classifier 1 F1", f1_score(y_true=y_test, y_pred=y_test_svc))

    # классификатор 2
    svc_model_2 = svm.SVC(kernel="rbf", gamma="auto", class_weight="balanced")
    svc_model_2.fit(x_train, y_train)
    y_test_svc_2 = svc_model_2.predict(x_test)
    print("Classifier 2 F1", f1_score(y_true=y_test, y_pred=y_test_svc_2))

    # классификатор 3
    nca = make_pipeline(StandardScaler(), NeighborhoodComponentsAnalysis(n_components=2, random_state=0))
    knn = KNeighborsClassifier(n_neighbors=3)
    nca.fit(x_train, y_train)
    knn.fit(nca.transform(x_train), y_train)
    y_test_knn = knn.predict(nca.transform(x_test))
    print("Classifier 3 F1", f1_score(y_true=y_test, y_pred=y_test_knn))
