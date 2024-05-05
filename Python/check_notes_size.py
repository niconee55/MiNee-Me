# Print how many notes are in the file
with open("./train_notes.txt", "r") as file:
    text = file.read()

# Split the notes into individual notes
notes_list = text.split()



# Filter out the notes that are greater than 90 or less than 30
filtered_notes = [note for note in notes_list if 40 <= int(note) <= 80]

print("Before filtering:", len(notes_list))
print("After filtering:", len(filtered_notes))


# Get 5 notes that are played the most and use them as the first 5 input notes
notes_played = {}
for note in notes_list:
    notes_played[note] = notes_played.get(note,0)+1
top_notes = sorted(notes_played.items(), key=lambda x: x[1], reverse=True)[:5]
input_notes = [note for note, _ in top_notes]
input_notes = ' '.join(note for note, _ in top_notes)   
print(input_notes) 
