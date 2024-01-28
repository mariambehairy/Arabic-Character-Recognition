# -*- coding: utf-8 -*-
"""Arabic Character Recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YUqUmMCisEwuTw7vfR6gMiDLCvpzzZr8
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model

from sklearn.model_selection import train_test_split , StratifiedKFold
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.neighbors import KNeighborsClassifier

"""Data exploration and preparation"""

df= pd.read_csv(r"C:\Users\maria\Downloads\csvTrainImages 13440x1024.csv",header=None)
df_labels=pd.read_csv(r"C:\Users\maria\Downloads\csvTrainLabel 13440x1.csv",header=None )
images = df.to_numpy()
normalized_images=images/255.

df_test = pd.read_csv(r"C:\Users\maria\Downloads\csvTestImages 3360x1024.csv",header=None)
df_labels_test = pd.read_csv(r"C:\Users\maria\Downloads\csvTestLabel 3360x1.csv",header=None)
df_labels_test.to_numpy
images_t = df_test.to_numpy()
images_test=images_t/255.

unique_classes = df_labels[0].unique()
print("Unique Classes:", unique_classes)

class_distribution = df_labels[0].value_counts()
plt.figure(figsize=(10, 6))
class_distribution = class_distribution.sort_index()
class_distribution.plot(kind='bar', color='skyblue')
plt.title('Alphabets Classes Distribution')
plt.xlabel('Alphabets Class')
plt.ylabel('Count')
plt.show()

def display_image(image):
    image_size = 32
    images = image.reshape((image_size, image_size))
    plt.imshow(images, cmap='gray')
    plt.axis('off')
    plt.show()

display_image(images[0])
display_image(images[3])
display_image(images[54])
display_image(images[80])

df_labels = df_labels.to_numpy()
df_labels_test = df_labels_test.to_numpy()
print(df_labels.dtype)
print(df_labels_test.dtype)

"""First Experiment Support Vector Machine (SVM)"""

X_train, X_test, y_train, y_test = train_test_split(normalized_images, df_labels, test_size=0.2, random_state=42)
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
kernel_accuracies = {kernel: [] for kernel in kernels}
for train_index, val_index in kf.split(X_test, y_test):
    X_val_train, X_val_test = X_test[train_index], X_test[val_index]
    y_val_train, y_val_test = y_test[train_index], y_test[val_index]
    for kernel in kernels:
        svm_model = SVC(kernel=kernel)
        svm_model.fit(X_val_train, y_val_train.ravel())
        y_val_pred = svm_model.predict(X_val_test)
        accuracy = accuracy_score(y_val_test.ravel(), y_val_pred)
        kernel_accuracies[kernel].append(accuracy)
for kernel, accuracies in kernel_accuracies.items():
    plt.plot(accuracies, label=f'Kernel: {kernel}')
plt.xlabel('Fold')
plt.ylabel('Accuracy')
plt.title('Accuracy Curve for Different Kernels over Different Folds')
plt.legend()
plt.show()

"""After splitting test data into 10 K-folds and test each kernel in each fold , we found that when kernel = 'rbf' ,The model performace is the highest"""

# Train an SVM model on training data
SVM_model = SVC(kernel='rbf', C=1.0, random_state=42)
SVM_model.fit(normalized_images, df_labels.ravel())

# Test the model on the test data
predictions_svm = SVM_model.predict(images_test)

# confusion matrix
conf_matrix = confusion_matrix(df_labels_test.ravel(), predictions_svm)
plt.figure(figsize=(10,8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=unique_classes, yticklabels=unique_classes)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# average f1-score
average_f1_score_svm = f1_score(df_labels_test.ravel(), predictions_svm, average='micro')
print("Average F1 Score:", average_f1_score_svm)

"""Second Experiment KNN"""

X_train, X_val, y_train, y_val = train_test_split(normalized_images, df_labels, test_size=0.1, random_state=42,shuffle=True)

encoder = OneHotEncoder(sparse=False, categories='auto')
y_train_onehot = encoder.fit_transform(y_train)
y_val_onehot = encoder.transform(y_val)

def train_and_evaluate_knn(X_train, y_train, X_val, y_val, k_values):
    f1_scores = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_val_pred = knn.predict(X_val)
        f1 = f1_score(y_val, y_val_pred, average='weighted')
        f1_scores.append(f1)
        print(f"K={k}, F1 Score (weighted): {f1}")

    return f1_scores

k_values = [1, 3, 5, 7, 9]
average_f1_scores = train_and_evaluate_knn(X_train, y_train_onehot, X_val, y_val_onehot, k_values)

plt.plot(k_values, average_f1_scores, marker='o')
plt.title('Average F1 Score with Different K Values')
plt.xlabel('K Value')
plt.ylabel('Average F1 Score')
plt.show()

best_k = k_values[np.argmax(average_f1_scores)]
print(f"The best K value is: {best_k}")

final_knn_model = KNeighborsClassifier(n_neighbors=best_k)
final_knn_model.fit(X_train, y_train_onehot)

y_test_onehot = encoder.transform(df_labels_test)
y_test_pred = final_knn_model.predict(images_test)
f1_test = f1_score(y_test_onehot, y_test_pred, average='weighted')

print(f"\nTest F1 Score (weighted): {f1_test}")

y_test_true_onehot = encoder.transform(df_labels_test)
conf_matrix = confusion_matrix(y_test_true_onehot.argmax(axis=1), y_test_pred.argmax(axis=1))

plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=unique_classes, yticklabels=unique_classes)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

"""Third Experiment Neural Network (NN)"""

def build_model_1(input_shape):
    model = Sequential()
    model.add(tf.keras.layers.Dense(32, input_shape=input_shape, activation='relu'))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(32, activation='relu'))
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dense(28, activation='softmax'))
    return model

def build_model_2(input_shape):
    model = Sequential()
    model.add(tf.keras.layers.Dense(128, input_shape=input_shape, activation='relu'))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(420, activation='relu'))
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dense(612, activation='relu'))
    model.add(tf.keras.layers.Dense(612, activation='relu'))
    model.add(tf.keras.layers.Dense(28, activation='softmax'))
    return model

X_train, X_val, y_train, y_val = train_test_split(normalized_images, df_labels, test_size=0.05, random_state=42,shuffle=True)

encoder = OneHotEncoder(sparse=False, categories='auto')
y_train_onehot = encoder.fit_transform(y_train)
y_val_onehot = encoder.transform(y_val)

def train_and_plot(model, X_train, y_train, X_val, y_val, model_name):
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Add a ModelCheckpoint callback to save the best model
    checkpoint = ModelCheckpoint(model_name, monitor='val_accuracy', save_best_only=True)

    history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_val, y_val), callbacks=[checkpoint])

    # Plot training and validation curves
    plt.plot(history.history['accuracy'], label='train_accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.legend()
    plt.show()

# Reshape input data if needed
input_shape = X_train.shape[1:]

# Example usage
model_1 = build_model_1(input_shape)
train_and_plot(model_1, X_train, y_train_onehot, X_val, y_val_onehot, 'model_1.h5')

model_2 = build_model_2(input_shape)
train_and_plot(model_2, X_train, y_train_onehot, X_val, y_val_onehot, 'model_2.h5')

best_model = load_model('model_2.h5')
y_pred_probabilities = best_model.predict(images_test)
y_pred_classes = np.argmax(y_pred_probabilities, axis=1)
y_pred_classes+=1

accuracy = accuracy_score(df_labels_test, y_pred_classes)
f1 = f1_score(df_labels_test, y_pred_classes, average='weighted')

print("Accuracy:", accuracy)
print("\nF1 Score (weighted):", f1)

conf_matrix = confusion_matrix(df_labels_test, y_pred_classes)
plt.figure(figsize=(10,8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=unique_classes, yticklabels=unique_classes)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()
plt.show()
plt.show()