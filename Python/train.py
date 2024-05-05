#------------------------------------------------------------------
# IW python portion
# train.py
# Authors: Nicolas Nee
# This file accepts a string of notes as an input file and trains
# a model off of it.
#------------------------------------------------------------------
import random
import pickle
import numpy as np
import pandas as pd
import os
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Activation, Dropout
from tensorflow.keras.optimizers import RMSprop
import time

# Map all the notes to 4th octave
def map(notes_list):
    mapped_notes = []
    for note in notes_list:
        note = int(note)
        if note % 12 == 0:
            note = 60
        if note % 12 == 1:
            note = 61
        if note % 12 == 2:
            note = 62
        if note % 12 == 3:
            note = 63
        if note % 12 == 4:
            note = 64
        if note % 12 == 5:
            note = 65
        if note % 12 == 6:
            note = 66
        if note % 12 == 7:
            note = 67
        if note % 12 == 8:
            note = 68
        if note % 12 == 9:
            note = 69
        if note % 12 == 10:
            note = 70
        if note % 12 == 11:
            note = 71
        mapped_notes.append(str(note))
    return mapped_notes

def train():
    start_time = time.time()
    file_path = 'train_notes.txt'
    with open(file_path, "r") as file:
        text = file.read()

    # Split the notes into individual notes
    # notes_list = text.split()

    # Filter out the notes that are greater than 80 or less than 40
    # filtered_notes = [note for note in notes_list if 40 <= int(note) <= 80]
    
    # Map all the notes to the 4th octave
    # mapped_notes = map(notes_list)
        
    # notes = ' '.join(filtered_notes)
    # notes = ' '.join(mapped_notes)
    notes = text

    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(notes)
    unique_tokens = np.unique(tokens)
    print(unique_tokens)

    unique_token_index = {token: index for index, token in enumerate(unique_tokens)}

    # look at the previous n notes
    n = 10
    input_notes = [] 
    next_note = []

    for i in range(len(tokens) - n):
        input_notes.append(tokens[i:i+n])
        next_note.append(tokens[i+n])

    X = np.zeros((len(input_notes), n, len(unique_tokens)), dtype = bool)
    Y = np.zeros((len(next_note), len(unique_tokens)), dtype = bool)

    for i, notes in enumerate(input_notes):
        for j, note in enumerate(notes):
            X[i,j, unique_token_index[note]] = True
        Y[i, unique_token_index[next_note[i]]] = True

    model = Sequential()
    model.add(LSTM(128, input_shape=(n, len(unique_tokens)), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dense(len(unique_tokens)))
    model.add(Activation("softmax"))

    model.compile(loss="categorical_crossentropy", 
                optimizer = RMSprop(learning_rate=0.01),
                metrics = ["accuracy"])
    history = model.fit(X,Y, batch_size = 128, epochs = 11, shuffle = True, validation_split=0.2)
    
    # Plotting the loss and accuracy from the training history
    epochs = range(1, len(history.history['loss']) + 1)

    # Plot Loss
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, history.history['loss'], 'b', label='Training Loss')
    plt.plot(epochs, history.history['val_loss'], 'r', label='Validation Loss')  # If you have validation data
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # Plot Accuracy
    plt.subplot(1, 2, 2)
    plt.plot(epochs, history.history['accuracy'], 'b', label='Training Accuracy')
    plt.plot(epochs, history.history['val_accuracy'], 'r', label='Validation Accuracy')  # If you have validation data
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()
    
    
    
    
    save_file_path = 'Python/unfilteredModelPlot.h5'
    model.save(save_file_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Ellapsed time:", elapsed_time)
    
if __name__ == '__main__':
    train()