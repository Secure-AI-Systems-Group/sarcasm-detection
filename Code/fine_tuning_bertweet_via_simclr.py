# -*- coding: utf-8 -*-
"""Fine-Tuning BERTweet via SimCLR

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WCshW7rn96NOCRXaUmfpBh_XSgXe8vXe

## Imports:
"""

!pip install transformers
!pip install -q bitsandbytes
!pip install pytorch_metric_learning
!pip install sentencepiece
import pandas as pd
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel

import bitsandbytes as bnb

from tqdm import tqdm
from operator import itemgetter
from pytorch_metric_learning.losses import NTXentLoss

!pip install accelerate -U

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

import torch
print(torch.cuda.is_available())

"""## Data Importing:"""

# Importing Train
import pickle
!gdown https://drive.google.com/uc?id=1BkLAz1cBh_0HtL2Xqk-foMeWyPC1q24m
with open("SarcasmTrain", "rb") as fp:
  train_data = pickle.load(fp)

# Importing Test
import pandas as pd
!gdown https://drive.google.com/uc?id=1Z2UZuOlLYsH5wQks3matPA3J_dRTi9RR
test_data = pd.read_csv("/content/SarcasmTest.csv")
test_data.drop('Unnamed: 0', axis = 1, inplace = True)

test_data

# Creating a dictionairy for the test_data so it can be used in the data loader
test_data_dict = {}
sarcastic_test = list(test_data['Sarcastic'])
non_sarcastic_test = list(test_data['Non-Sarcastic'])
for i in range(0, 1067):
  temp_non_sarcasm = []
  temp_non_sarcasm.append(non_sarcastic_test[i])
  test_data_dict[sarcastic_test[i]] = temp_non_sarcasm

"""## Data Loader:"""

from torch.utils.data import Dataset
from transformers import RobertaTokenizer
import random

class MyDataset(Dataset):
  def __init__(self, data):
    self.data = data
    self.keys = list(data.keys())
    self.data_length = len(self.keys)

  def __len__(self):
    return self.data_length

  def __getitem__(self, idx):
    negative = self.keys[idx]
    anchor = random.choice(self.data[negative])
    positive = self.select_positive(idx)
    return anchor, positive, negative

  def select_positive(self, negative_idx):
    while True:
      positive_idx = negative_idx
      while positive_idx == negative_idx:
        positive_idx = random.choice(range(self.data_length))
      return random.choice(self.data[self.keys[positive_idx]])

"""## Config File (Centralizes all the hyperparameters):"""

class config:
  batch_size = 50
  num_workers = 4
  text_encoder_lr = 1e-5
  weight_decay = 1e-3
  epochs = 10
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

  model_name = 'vinai/bertweet-base'
  text_embedding = 768
  max_length = 510
  embedding_size = 768
  hidden_size = 256

  pretrained = True
  trainable_language = True
  trainable_logic = True
  temperature = .7

  num_projection_layers = 2
  projection_dim = 256
  dropout = 0.01

"""## Modules:"""

from transformers import RobertaModel, RobertaTokenizer
# Used to encode the inputs using RoBERTa

class Encoder(torch.nn.Module):
  def __init__(self, model_name, trainable):
    super().__init__()
    self.model = RobertaModel.from_pretrained(model_name)
    for param in self.model.parameters():
      param.requires_grad = trainable

  def forward(self, input_ids, attention_mask):
    outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
    last_hidden_state = outputs[0]
    pooled_output = last_hidden_state.mean(dim=1)
    return pooled_output

# Used to reduce the dimensionality of RoBERTa outputs and get it ready for classification task

class ProjectionHead(torch.nn.Module):
  def __init__(self, input_dim, output_dim, dropout_rate):
    super().__init__()

    self.projection = torch.nn.Sequential(
      torch.nn.Linear(input_dim, output_dim),
      torch.nn.ReLU(),
      torch.nn.Dropout(dropout_rate),
      torch.nn.Linear(output_dim, output_dim)
    )

  def forward(self, x):
    return self.projection(x)

from pytorch_metric_learning.losses import NTXentLoss

class SimCLR(nn.Module):
  def __init__(self, encoder, projection_head, temperature):
    super(SimCLR, self).__init__()
    self.encoder = encoder
    self.projection_head = projection_head
    self.temperature = temperature
    self.loss_fn = NTXentLoss(temperature)

  def forward(self, anchor_input, positive_input, negative_input):
    z_i = self.projection_head(self.encoder(**anchor_input))
    z_j = self.projection_head(self.encoder(**positive_input))
    z_k = self.projection_head(self.encoder(**negative_input))
    out = torch.cat([z_i, z_j], dim=0)
    labels = torch.cat([torch.arange(z_i.size(0)), torch.arange(z_i.size(0))], dim=0).to(z_i.device)

    return out, labels

  def get_loss(self, anchor_input, positive_input, negative_input):
    out, labels = self.forward(anchor_input, positive_input, negative_input)
    loss = self.loss_fn(out, labels)
    return loss

"""## SimCLR Embeddings Generation Via SimCLR Framework and BERTweet:"""

!pip install emoji

import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer

encoder = Encoder(config.model_name, config.trainable_language)
projection_head = ProjectionHead(config.text_embedding, config.projection_dim, config.dropout)
simclr_model = SimCLR(encoder, projection_head, config.temperature)
simclr_model = simclr_model.to(config.device)

tokenizer = AutoTokenizer.from_pretrained(config.model_name)
if not tokenizer.pad_token:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
my_dataset = MyDataset(train_data)
data_loader = DataLoader(my_dataset, batch_size=config.batch_size, shuffle=True)

optimizer = torch.optim.Adam(simclr_model.parameters(), lr=config.text_encoder_lr, weight_decay=config.weight_decay)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

for epoch in range(config.epochs):
  epoch_loss = 0
  for anchor, positive, negative in data_loader:
    anchor_input = {key: val.to(config.device) for key, val in tokenizer(anchor, return_tensors="pt", padding='longest', truncation=True).items() if key != 'token_type_ids'}
    positive_input = {key: val.to(config.device) for key, val in tokenizer(positive, return_tensors="pt", padding='longest', truncation=True).items() if key != 'token_type_ids'}
    negative_input = {key: val.to(config.device) for key, val in tokenizer(negative, return_tensors="pt", padding='longest', truncation=True).items() if key != 'token_type_ids'}

    loss = simclr_model.get_loss(anchor_input, positive_input, negative_input)
    epoch_loss += loss.item()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

  scheduler.step()

  print(f"Epoch {epoch+1}, Loss: {epoch_loss}")

  torch.save(simclr_model.state_dict(), f'BERTweet_simclr_model_epoch_{epoch+1}.pth')

from google.colab import drive
drive.mount('/content/drive')
import shutil
shutil.copy("/content/BERTweet_simclr_model_epoch_10.pth","/content/drive/MyDrive/Contrastive NLP Stuff/Data/Models/")