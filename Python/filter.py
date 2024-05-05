from mido import MidiFile
import serial
import time
import sys
from remove_dups import remove_dups

def get_notes(mid, notes = ""):
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' or msg.type =='note_off':
                if msg.note >= 60 and msg.note <= 77:
                    notes += str(msg.note) + " "
    return notes

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

if len(sys.argv) != 2:
    print("Usage: needs a midi file")
    sys.exit(1)
        
midi_file_path = sys.argv[1]
mid = remove_dups(midi_file_path)
notes = get_notes(mid)
notes = ' '.join(map(notes.split()))

with open("mr_brightside.txt", "w") as file:
    # Write the string to the file
        file.write(notes)