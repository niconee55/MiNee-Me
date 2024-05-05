import os
import sys
from mido import MidiFile, MidiTrack, Message

def remove_sharps(notes):
    valid_notes = ['60', '62', '64', '65', '67', '69', '71']
    return_notes = []
    for note in notes:
        if note in valid_notes:
            return_notes.append(note)
    return return_notes

# Save the midi file with a different note into a new file
def main():
    output_file_path = 'mid_files/generations/evenLessNoCreativePrev2.mid'
    
    
    text_file_path = 'generated_notes.txt'
    with open(text_file_path, "r") as file:
        notes_file = file.read()
        
    notes = notes_file.split()
    
    # notes = remove_sharps(notes)
    
    notes_played = {}
    modified_track = MidiTrack()
    
    time = 240
    channel = 0

    for note in notes:
        notes_played[note] = notes_played.get(note,0)+1
        
        velocity = 0
        note_command = "note_off"
        # if odd, play note by changing velocity
        if notes_played[note] % 2 == 1:
            velocity = 100
            note_command = "note_on"
        
        msg = Message(note_command, note = int(note), velocity = int(velocity), 
                      time = time, channel = channel)
        modified_track.append(msg)

    
    modified_midi = MidiFile()
    modified_midi.tracks.append(modified_track)
    print(modified_midi)
    
    modified_midi.save(output_file_path)

if __name__ == '__main__':
    main()