# Arabic-Character-Recognition
This project focuses on classifying Arabic handwritten characters using various machine learning models, including SVM, KNN, and Neural Networks. The dataset comprises flattened pixels extracted from images of Arabic characters. The goal is to explore the data, preprocess it, train different models, and compare their performances.

Data Exploration and Preparation  

Unique Classes and Sample Distribution  
* Identify the number of unique classes.  
* Examine the distribution of samples in each class.

Image Normalization and Visualization  
* Normalize each image in the dataset.  
* Write a function to reconstruct and display images from flattened vectors.  
* Visualize some images in the dataset using the reconstruction function.

Experiments and Results  

First Experiment: SVM Model  
* Train an SVM model on the training data.  
* Test the SVM model.
* Provide the confusion matrix.
* Calculate the average F-1 scores for the testing dataset.
* Split Training Data
* Split the training data into training and validation datasets.

Second Experiment: KNN Models
* Try different K values with KNN models.
* Plot the average F-1 scores with the validation dataset using different K values.
* Suggest the best value for K.
* Test the KNN model with the best K value.
* Provide the confusion matrix.
* Calculate the average F-1 scores for the testing dataset.

Third Experiment: Neural Network Models
* Build two different Neural Network model architectures.
* Train each model and plot error and accuracy curves for training and validation data.
* Save the best model and reload it.
* Use the best model on new unlabeled data to get predictions.
* Test the best model.
* Provide the confusion matrix.
* Calculate the average F-1 scores for the testing dataset.
* Model Comparison and Conclusion

Compare the results of the SVM, KNN, and Neural Network models.  
Suggest the best model based on performance metrics.
