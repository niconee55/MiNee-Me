#------------------------------------------------------------------
# IW python portion
# midiRead.py
# Authors: Nicolas Nee
# This file accepts a string of notes as an input file and trains
# a model off of it.
#------------------------------------------------------------------
import random
import pickle
import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Activation
from tensorflow.keras.optimizers import RMSprop
import os

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

def predict_next_word(test_notes, n_best, unique_tokens, 
                      unique_token_index, model):
    n = 10
    X_predict = np.zeros((1, n, len(unique_tokens)))
    for i, note in enumerate(test_notes.split()):
        X_predict[0, i, unique_token_index[note]] = 1
    predictions = model.predict(X_predict)[0]
    return np.argpartition(predictions, n_best)[n_best:]

# creativity: choose from 3 most likely choices
def generate_notes(input_notes, output_length, tokenizer, model,
                   unique_tokens, unique_tokens_index, creativity=1, n=3):

    note_sequence = input_notes.split()
    current = 0
    for _ in range(output_length):
        sub_seq = " ".join(tokenizer.tokenize(" ".join(note_sequence))[current:current+n])
        try:
            choice = unique_tokens[
                random.choice(predict_next_word(sub_seq, creativity, 
                                                unique_tokens, unique_tokens_index, 
                                                model))]
        except:
            print("Getting random choice")
            choice = random.choice(unique_tokens)
        note_sequence.append(choice)
        current += 1
    return " ".join(note_sequence)

def main():

    text_file_path = 'train_notes.txt'
    model_file_path = 'Python/unfilteredEvenLessModel.h5'

    with open(text_file_path, "r") as file:
        text = file.read()
    note_string = text.split()    

    # Filter out the notes that are greater than 40 or less than 80
    # filtered_notes = [note for note in note_string if 40 <= int(note) <= 80]

    # Map all the notes to the 4th octave
    # mapped_notes = map(note_string)

    # notes = ' '.join(filtered_notes)
    # notes = ' '.join(mapped_notes)
    notes = text
    
    # Get 5 notes that are played the most and use them as the first 5 input notes
    notes_played = {}
    for note in note_string:
        notes_played[note] = notes_played.get(note,0)+1
    top_notes = sorted(notes_played.items(), key=lambda x: x[1], reverse=True)[:10]
    input_notes = [note for note, _ in top_notes]
    input_notes = ' '.join(note for note, _ in top_notes)   
    print(input_notes) 
    
    model = load_model(model_file_path)
    model.compile(loss="categorical_crossentropy", 
              optimizer = RMSprop(learning_rate=0.01),
              metrics = ["accuracy"])

    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(notes)
    unique_tokens = np.unique(tokens)
    unique_token_index = {token: index for index, token in enumerate(unique_tokens)}
    
    generated_notes = generate_notes(input_notes, 100, tokenizer, model,
                   unique_tokens, unique_token_index)
    print("\n\nnotes generated to generated_notes.txt")
    # print(generated_notes)
    with open("generated_notes.txt", "w") as file:
    # Write the string to the file
        file.write(generated_notes)
        
    
if __name__ == '__main__':
    main()
        