import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split

from sklearn.neural_network import MLPClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import BaggingClassifier, StackingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import numpy as np

# Reading Wisconsin Breast Cancer Dataset
data = pd.read_csv('cancer.csv')
classifierList = ["Naive Bayes", "Decision Tree", "Ensemble Decision Tree", "K-Nearest Neighbor", "Ensemble KNN", "Hierarchical Ensemble"]
accuracyList = []

def dataPreProcessing():
    # Dropping unwanted columns
    data.drop(['id'], axis=1, inplace=True)
    # Replacing missing values with zero
    data.replace('?', 0, inplace=True)
    # Changing data into NumPy arrays
    values = data.values
    # Now impute it to replace missing values
    imputer = SimpleImputer()
    imputedData = imputer.fit_transform(values)
    # Normalizing the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    normalizedData = scaler.fit_transform(imputedData)

    return normalizedData


def compareClassifiers(receivedData):
    # Segregate the features from the labels
    X = receivedData[:, 0:9]
    Y = receivedData[:, 9]
    num_trees = 20
    dfData = pd.DataFrame(data=X)
    dfLabels = pd.DataFrame(data=Y)
    # splitting data for traning and testing
    X_train, X_test, y_train, y_test = train_test_split(dfData, dfLabels, test_size=0.33, random_state=77)
    dash = "-"

    gnb = GaussianNB()
    fittedGNB = gnb.fit(X_train, y_train.values.ravel())
    print("{0}\n{1}".format("Naive Bayes Classifier", dash * 22))
    calculateMetrics(fittedGNB, X_test, y_test)

    # generating conventional Decision tree classifier
    DT_model = DecisionTreeClassifier(criterion='entropy', max_depth=5, min_samples_split=0.2, min_samples_leaf=0.2)
    fittedDT = DT_model.fit(X_train, y_train.values.ravel())
    print("{0}\n{1}".format("Decision Tree Classifier", dash * 24))
    calculateMetrics(fittedDT, X_test, y_test)

    # generating decision tree ensembles
    DTBagging = BaggingClassifier(base_estimator=DT_model, n_estimators=num_trees, random_state=7)
    fittedDTB = DTBagging.fit(X_train, y_train.values.ravel())
    print("{0}\n{1}".format("Ensemble Decision Tree Classifier", dash * 33))
    calculateMetrics(fittedDTB, X_test, y_test)

    # generating conventional k-Nearest Neighbour classifier
    KNN_model = KNeighborsClassifier(n_neighbors=2)
    fittedKNN = KNN_model.fit(X_train, y_train.values.ravel())
    print("{0}\n{1}".format("k-Nearest Neighbour Classifier", dash * 30))
    calculateMetrics(fittedKNN, X_test, y_test)

    # generating k-Nearest Neighbour ensembles
    KNNBagging = BaggingClassifier(base_estimator=KNN_model, n_estimators=num_trees, random_state=7)
    fittedKNNB = KNNBagging.fit(X_train, y_train.values.ravel())
    print("{0}\n{1}".format("Ensemble k-Nearest Neighbour Classifier", dash * 39))
    calculateMetrics(fittedKNNB, X_test, y_test)

    # Neural Network is used as final estimator for Stacking Classifier
    neuralNetwork_model = MLPClassifier(solver='lbfgs', alpha=1e-5,
                                        hidden_layer_sizes=(3,), random_state=1, max_iter=5000)
    estimators = []
    estimators.append(('DecisionTreeBagging', DTBagging))
    estimators.append(('KNNBagging', KNNBagging))

    # used stacking classifier as a heterogeneous bagging classifier
    ensemble = StackingClassifier(estimators=estimators,final_estimator=neuralNetwork_model)
    fittedensemble = ensemble.fit(X_train, y_train.values.ravel())
    print("{0}\n{1}".format("Hierarchical Ensemble Classifier", dash * 32))
    calculateMetrics(fittedensemble, X_test, y_test)

    return accuracyList


def calculateMetrics(trainedReceivedClassifier, XtestData, YtestData):
    # Confusion matrix is used to find the correctness and accuracy of the model
    # It is used for Classification problem where the output can be of two or more types of classes.
    predictor = trainedReceivedClassifier.predict(XtestData)
    confusionMatrix = confusion_matrix(predictor, YtestData)

    # Accuracy in classification problems is the number of correct predictions made by the model over all kinds predictions made.
    # In the Numerator, are our correct predictions (True positives and True Negatives)and in the denominator, are the kind of all predictions made by the algorithm.
    accuracy = accuracy_score(predictor, YtestData)
    accuracyList.append(accuracy*100)

    # ROC is a probability curve and AUC represents degree or measure of separability
    # It tells how much model is capable of distinguishing between classes.
    rocaucScore = roc_auc_score(YtestData, predictor, average="macro")  # AUC-ROC score

    # classification report contains Precision, Recall, f1-score and support
    # Precision: Precision is the proportion of relevant results
    # Recall: percentage of total relevant results correctly classified by the algorithm.
    # f1-score: This is the combination of both Precision and Recall (Harmonic mean of the both)
    # Support: The number of true instances for each label
    ClassificationReport = classification_report(predictor, YtestData)
    print("Accuracy : ", accuracy)
    print("ROC_AUC Score :", rocaucScore)
    print("Classification Report :")
    print(ClassificationReport)
    print("Confusion Matrix: ")
    print("{0}{1:20}{2:20}".format(" "*17, "Class_1_Predicted", "Class_2_Predicted"))
    print("{0:10}{1:15}{2:15}".format("Class_1_Actual", confusionMatrix[0][0], confusionMatrix[0][1]))
    print("{0:10}{1:15}{2:15}".format("Class_2_Actual", confusionMatrix[1][0], confusionMatrix[1][1]))
    print("\n\n")



# plotting accuracy values of each classifiers
def plot():
    x = np.arange(len(classifierList))  # the label locations
    width = 0.4  # the width of the bars
    fig, ax = plt.subplots(figsize=(14, 7))
    rectangles = ax.bar(x - width / 48, receivedAccuracyList, width, edgecolor="black")
    ax.set_title('Accuracy Comparison between Classifiers', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(classifierList)
    label(rectangles,ax)
    plt.show()

# Labeling accuracy value on top of each bar
def label(rects,ax):
    for rect in rects:
        height = (rect.get_height())
        ax.annotate('{}%'.format(round(height, 2)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


preProcessedData = dataPreProcessing()
receivedAccuracyList = compareClassifiers(preProcessedData)
plot()












