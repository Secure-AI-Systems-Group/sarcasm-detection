# -*- coding: utf-8 -*-
"""SarcasmSIGN Data Cleaning

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18YSklm6Y0kgs55wz96mcz4SEzu-Q81bf

# SarcasmSIGN Training Dataset:
"""

# Downloading the SarcasmSIGN dataset
!gdown https://drive.google.com/uc?id=1kgKg-3_CmDZCT5HWUaweF30cj7Pu_3TR
!gdown https://drive.google.com/uc?id=19G6i6r_xy2d3G_j9etW_VEBQt0Nr-_CE

# Converting the test to a list of lists
import ast
test_list = []
with open("test.txt", 'r') as file:
  lines = file.readlines()

for i in lines:
  test_list.append(ast.literal_eval(i))

# Converting the train to a list of lists
train_list = []
with open("train.txt", 'r') as file:
  lines = file.readlines()

for i in lines:
  train_list.append(ast.literal_eval(i))

# Combining train and test into one large dataset
data_list = train_list + test_list

data_list[13459:13464]

# Creating a list of list to store the data
new_data_list = [[' best day of my life', ' worst day of my life']]
counter = 0
for i in range(1, 13470):
  if(data_list[i - 1][0] == data_list[i][0]):
    new_data_list[counter].append(data_list[i][1])
  else:
    counter += 1
    new_data_list.append([data_list[i][0], data_list[i][1]])

# Removing the occurences that have the same sarcastic text and same translations
same_occurences = 0
temp_list = []
for i in new_data_list:
  if (len(set(i)) == 1):
    same_occurences += 1
  else:
    temp_list.append(i)

print(same_occurences)
new_data_list = temp_list

# Converting it to a dictionairy
train_dict = {}
for i in new_data_list:
  train_dict[i[0]] = i[1:]

# Some translations have duplicates so we'll remove those
for i in train_dict.keys():
  temp = []
  temp.append(i)
  train_dict[i] = list(set(train_dict[i]).difference(set(temp)))
  train_dict[i] = list(set(train_dict[i]))

# Download the dictionairy as a binary file to allow for ease of getting it during the training process
import pickle
with open("SarcasmTrain", "wb") as fp:
  pickle.dump(train_dict, fp)

from google.colab import drive
drive.mount('/content/drive')
import shutil

shutil.copy("/content/SarcasmTrain","/content/drive/MyDrive/Contrastive NLP Stuff/Data/SimCLR Model Training Data/")