#------------------------------------------------------------------
# IW python portion
# get_notes.py
# Authors: Nicolas Nee
#------------------------------------------------------------------

# Helper function that iterates over a double list and checks if 
# It already contains the note
def contains_note(notes, note):
    for index, note_info in enumerate(notes):
        if note_info[0] == note:
            return index
    return None

# Helper function that iterates over a double list and checks if
# it already contains the time
def contains_time(notes, time):
    for index, note_info in enumerate(notes):
        if note_info[0] == time:
            return index
    return None

# take in the midi track and return a double list with each note and the 
# times that they are used (pressed and unpressed).
def get_notes(track):
    notes = []
    total_time = 0
    for msg in track:
        if msg.type == 'note_on' or msg.type =='note_off':
            note = msg.note
            time = msg.time
            note_index = contains_note(notes, note)
            total_time += time
            # First time the note is played
            if note_index is None:
                notes.append([note, total_time])
            # The note has been played before. Add the time.
            else:
                notes[note_index].append(total_time)
    return notes, total_time

# Take in the midi track and return a double list with each time
# something happens and what note is used at that time
def get_times(track):
    times = []
    total_time = 0
    for msg in track:
        if (msg.type == 'note_on' or msg.type == 'note_off') and msg.channel == 0:
            note = msg.note
            time = msg.time
            total_time += time
            time_index = contains_time(times, total_time)
            # A note at this time is being played for the first time
            if time_index is None:
                times.append([total_time, note])
            else:
                times[time_index].append(note)
    return times, total_time
    
                