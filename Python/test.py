from mido import MidiFile, MidiTrack, Message
import sys

def map(note):
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
    return note

if len(sys.argv) != 2:
    print("Usage: needs a midi file")
    sys.exit(1)
original_midi_file_path = sys.argv[1]
mid = MidiFile(original_midi_file_path, clip = True)
modified_track = []
print(mid)
prev = None
for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                if prev is not None and (msg == prev):
                    print(msg)
                prev = msg
            
mid.save(original_midi_file_path)


