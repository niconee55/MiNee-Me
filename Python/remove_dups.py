import os
import sys
from mido import MidiFile

# Returns the mid file with duplicates removed
def remove_dups(original_midi_file_path):
    mid = MidiFile(original_midi_file_path, clip = True)

    message_numbers = []
    duplicates = []

    for track in mid.tracks:
        if len(track) in message_numbers:
            duplicates.append(track)
        else:
            message_numbers.append(len(track))

    for track in duplicates:
        mid.tracks.remove(track)

    return mid

# Saved the mid file with duplicates removed into a new file
def main():
    if len(sys.argv) != 2:
        print("Usage: needs a midi file")
        sys.exit(1)
    original_midi_file_path = sys.argv[1]
    output_midi_file_path = os.path.splitext(original_midi_file_path)[0] + "_filtered.mid"

    mid = MidiFile(original_midi_file_path, clip = True)

    message_numbers = []
    duplicates = []

    for track in mid.tracks:
        if len(track) in message_numbers:
            duplicates.append(track)
        else:
            message_numbers.append(len(track))

    for track in duplicates:
        mid.tracks.remove(track)

    mid.save(output_midi_file_path)
    
if __name__ == '__main__':
    main()