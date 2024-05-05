import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
from tensorflow.keras.models import load_model

def add_missing_notes(list):
    notes_to_exclude = ['118', '119', '120', '123', '124', '126']
    filtered_list = [note for note in list if note not in notes_to_exclude]
    filtered_list.extend(['125', '12', '14', '16', '19', '2', '20', '22', '23'])
    return filtered_list
    

model_file_path = 'Python/unfilteredEvenLessModel.h5'
model = load_model(model_file_path)

test_file_path = 'validate_notes.txt'
with open(test_file_path, "r") as file:
    test_notes = file.read()

# Split the notes into individual notes
test_notes_list = test_notes.split()
test_notes_list = add_missing_notes(test_notes_list)
test_notes = ' '.join(test_notes_list)

test_tokenizer = RegexpTokenizer(r"\w+")
test_tokens = test_tokenizer.tokenize(test_notes)
test_unique_tokens = np.unique(test_tokens)
print(test_unique_tokens)

test_unique_token_index = {token: index for index, token in enumerate(test_unique_tokens)}

n = 3
test_input_notes = [] 
test_next_note = []

for i in range(len(test_tokens) - n):
    test_input_notes.append(test_tokens[i:i+n])
    test_next_note.append(test_tokens[i+n])
    
X_TEST = np.zeros((len(test_input_notes), n, len(test_unique_tokens)), dtype = bool)
Y_TEST = np.zeros((len(test_next_note), len(test_unique_tokens)), dtype = bool)

for i, notes in enumerate(test_input_notes):
    for j, note in enumerate(notes):
        X_TEST[i,j, test_unique_token_index[note]] = True
    Y_TEST[i, test_unique_token_index[test_next_note[i]]] = True

evaluation = model.evaluate(X_TEST, Y_TEST, batch_size = 128)

print("Loss:", evaluation[0])
print("Accuracy:", evaluation[1])

# Plotting the loss and accuracy from the training history
epochs = range(1, len(model.history['loss']) + 1)

# Plot Loss
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(epochs, model.history['loss'], 'b', label='Training Loss')
plt.plot(epochs, model.history['val_loss'], 'r', label='Validation Loss')  # If you have validation data
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# Plot Accuracy
plt.subplot(1, 2, 2)
plt.plot(epochs, model.history['accuracy'], 'b', label='Training Accuracy')
plt.plot(epochs, model.history['val_accuracy'], 'r', label='Validation Accuracy')  # If you have validation data
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()