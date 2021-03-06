import cv2
import numpy as np
import pandas as pd 
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from sklearn.utils import compute_class_weight
#%matplotlib inline

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report,confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Activation, Conv2D, MaxPool2D, AveragePooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import SGD, RMSprop, Adam

print("Num GPUs Available: ", tf.config.experimental.list_physical_devices('GPU'))

#pip install numba 

# from numba import cuda

# cuda.select_device(0)
# cuda.close()

wiki_process =  pd.read_csv("data/dataset.csv")

wiki_process.head()

start = time.time()
try:  
    with tf.device('/device:GPU:7'):
        image_list = []
        for path in wiki_process["img_path"]:
            img = cv2.imread("data/" + path,cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img,(200,200))
            image_list.append(img)
except RuntimeError as e:
  print(e)
end = time.time()
print("time taken for execution :- {}".format(end-start))

# wiki_process = wiki_process.head(500)
wiki_process["image"] = image_list
wiki_process.head()

wiki_process.info()

#plt.imshow(wiki_process["image"][39454])

#normalizing the pixel values
try:  
    with tf.device('/device:GPU:7'):
        x_data = np.array(image_list)/255
        y_data = wiki_process["gender"].to_numpy()
except RuntimeError as e:
  print(e)

x_data.shape

y_data.shape

# image_x will contain the original grayscale images 
x_data = x_data.reshape((x_data.shape[0],200,200,1))

print("x_data shape: {}".format(x_data.shape))
print("y_data shape: {}".format(y_data.shape))

train_x, test_x, train_y, test_y = train_test_split(x_data, y_data, test_size=0.33, random_state=42)

print("train_x shape: {}".format(train_x.shape))
print("train_y shape: {}\n".format(train_y.shape))

print("test_x shape: {}".format(test_x.shape))
print("test_y shape: {}".format(test_y.shape))

# num_subjects = np.unique(y_data).shape[0]
# print("Number of subjects: {}".format(np.unique(y_data).shape[0]))

# # Model

# if tf.config.experimental.list_physical_devices('GPU'):
#     strategy = tf.distribute.MirroredStrategy()
# else:  # use default strategy
#     strategy = tf.distribute.get_strategy() 
# print(strategy)

# try:  
#     with strategy.scope():
#         # specify the input size of the images
#         images = Input((train_x.shape[1], train_x.shape[2], 1,))
#         # a convolution layer of 32 filters of size 9x9 to extract features (valid padding)
#         x = Conv2D(64,kernel_size=(3,3),padding="valid")(images)
#         x = Conv2D(64,kernel_size=(3,3),padding="valid")(x)
        
#         # a maxpooling layer to down-sample features with pool size (2, 2)
#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)

#         x = Conv2D(128,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(128,kernel_size=(3,3),padding="valid")(x)

#         # a maxpooling layer to down-sample features with pool size (2, 2)
#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)

#         x = Conv2D(256,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(256,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(256,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(256,kernel_size=(3,3),padding="valid")(x)

#         # a maxpooling layer to down-sample features with pool size (2, 2)
#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)
        
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)

#         # a maxpooling layer to down-sample features with pool size (2, 2)
#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)
        
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)
#         x = Conv2D(512,kernel_size=(3,3),padding="valid")(x)
        
#         # a maxpooling layer to down-sample features with pool size (2, 2)
#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)
        
#         # flatten extracted features to form feature vector
#         x = Flatten()(x)

# #         # a drop out layer for regularization (25% probability)
# #         x = Dropout(rate=0.2,seed=0.25)(x)
        
#         first fully-connected layer to map the features to vectors of size 256
#         x = Dense(4096,activation="relu")(x)
#         x = Dense(4096,activation="relu")(x)
#         x = Dense(128,activation="relu")(x)
        
        
# #         # anoter drop out layer for regularization (25% probability)
# #         x = Dropout(rate=0.2,seed=0.25)(x)
        
#         # a second fully-connected layer to map the features to a logit vector with one logit per subject
#         x = Dense(1)(x)
#         # use softmax activation to convert the logits to class probabilities for each subject
#         predictions = Activation("sigmoid")(x)

#         # create the model using the layers we defined previously
#         sample_cnn = Model(inputs=images, outputs=predictions)

#         # compile the model so that it uses Adam for optimization during training with cross-entropy loss
#         sample_cnn.compile(optimizer=SGD(), loss="binary_crossentropy", metrics=["acc"])

#         # print out a summary of the model achitecture
#         print(sample_cnn.summary())

# except RuntimeError as e:
#   print(e)

# start = time.time()
# # class_weights = compute_class_weight("balanced", np.unique(train_y), train_y)
# # class_weights = dict(enumerate(class_weights))
# try:  
#     with tf.device('/device:GPU:4'):
#         # train model
#         history = sample_cnn.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=1,batch_size=150, verbose=1)
# except RuntimeError as e:
#   print(e)
# end = time.time()
# print("Time spent for training - {}".format(end-start))





# try:  
#     with tf.device('/device:GPU:5'):
#         test_pred = sample_cnn.predict(test_x)
#         for i in test_pred:
#             if i[0] >= 0.5:
#                 i[0] = 1
#             else:
#                 i[0] = 0
#         print(test_pred)
# except RuntimeError as e:
#   print(e)

# test_pred[test_pred<0.5]

# print(classification_report(test_y,test_pred))
# print(confusion_matrix(test_y,test_pred))

# test_y[0]

# for i in test_pred:
#     if i[0] >= 0.5:
#         i[0] = 1
#     else:
#         i[0] = 0
# test_pred

# history.history.keys()

# # summarize history for accuracy
# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()
# # summarize history for loss
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()

# sample_cnn.save("models/vgg19_model")

# batch norm SGD Model
chanDim = -1

try:  
    with tf.device('/device:GPU:7'):
        # specify the input size of the images
        images = Input((train_x.shape[1], train_x.shape[2], 1,))
        
        x= Conv2D(8, (3,3), padding="same")(images)
        x= Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= MaxPool2D(pool_size=(2,2),strides=2)(x)

        
        x = Conv2D(16,kernel_size=(3,3),padding="same")(x)
        x = Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= MaxPool2D(pool_size=(2,2),strides=2)(x)
        #x= Dropout(0.25)(x)

        x= Conv2D(32, (3,3), padding="same")(x)
        x= Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= MaxPool2D(pool_size=(2,2),strides=2)(x)
  
        
        x= Conv2D(64, (3,3), padding="same")(x)
        x= Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= MaxPool2D(pool_size=(2,2),strides=2)(x)
#         x= Dropout(0.25)(x)

        x= Conv2D(128, (3,3), padding="same")(x)
        x= Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= MaxPool2D(pool_size=(2,2),strides=2)(x)


        x= Conv2D(256, (3,3), padding="same")(x)
        x= Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= MaxPool2D(pool_size=(2,2),strides=2)(x)
#         x= Dropout(0.25)(x)
        
        x= Conv2D(512, (3,3), padding="same")(x)
        x= Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= MaxPool2D(pool_size=(2,2),strides=2)(x)

        x= Dropout(0.5)(x)

        x= Flatten()(x)
        x= Dense(1024)(x)
        x= Activation("relu")(x)
        x= BatchNormalization(axis=chanDim)(x)
        x= Dropout(0.5)(x)
        
        x= Dense(128)(x)
        x= Dropout(0.5)(x)


        x= Dense(1)(x)
        
        predictions = Activation("sigmoid")(x)

        # create the model using the layers we defined previously
        sample_cnn = Model(inputs=images, outputs=predictions)

        # compile the model so that it uses Adam for optimization during training with cross-entropy loss
        sample_cnn.compile(optimizer=SGD(), loss="binary_crossentropy", metrics=["acc"])

        # print out a summary of the model achitecture
        print(sample_cnn.summary())

except RuntimeError as e:
  print(e)

start = time.time()
# class_weights = compute_class_weight("balanced", np.unique(train_y), train_y)
# class_weights = dict(enumerate(class_weights))
try:  
    with tf.device('/device:GPU:7'):
        # train model
        history = sample_cnn.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=100,batch_size=100, verbose=1)
except RuntimeError as e:
  print(e)
end = time.time()
print("Time spent for training - {}".format(end-start))

try:  
    with tf.device('/device:GPU:7'):
        test_pred = sample_cnn.predict(test_x)
        for i in test_pred:
            if i[0] >= 0.5:
                i[0] = 1
            else:
                i[0] = 0
        print(test_pred)
except RuntimeError as e:
  print(e)

print(classification_report(test_y,test_pred))
print(confusion_matrix(test_y,test_pred))

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

sample_cnn.save("models/batch_norm_sgd")