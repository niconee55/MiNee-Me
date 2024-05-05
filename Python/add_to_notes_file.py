#------------------------------------------------------------------
# IW python portion
# add_to_notes_file.py
# Authors: Nicolas Nee
# Accepts a MIDI file as input and adds the notes to a file with 
# a string of notes in it to be tested off of
#------------------------------------------------------------------
import sys
from mido import MidiFile
from remove_dups import remove_dups

def add_to_file(notes):
    with open("validate_notes.txt", "a") as file:
    # Write the string to the file
        file.write(notes)
        print("Notes added!")

# Return how many notes are in the file
def check_notes_size():
    with open("validate_notes.txt", "r") as file:
        text = file.read()
    words = text.split()
    print("There are now", len(words), "notes")

def get_notes(mid, notes = ""):
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' or msg.type =='note_off':
                notes += str(msg.note) + " "
    return notes

def main():
    # MAKE SURE TO ADD A SPACE TO THE LAST NOTE
    if len(sys.argv) != 2:
        print("Usage: needs a midi file")
        sys.exit(1)
        
    midi_file_path = sys.argv[1]
    mid = remove_dups(midi_file_path)
    notes = get_notes(mid)
    add_to_file(notes)
    check_notes_size()

if __name__ == '__main__':
    main()