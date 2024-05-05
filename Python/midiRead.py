#------------------------------------------------------------------
# IW python portion
# midiRead.py
# Authors: Nicolas Nee
#------------------------------------------------------------------
from mido import MidiFile
import serial
import time
from get_notes import get_times
import sys
from remove_dups import remove_dups

# Helper function that iterates over all times and checks 
# whether there is a note played at current_time
def contains_time(times, current_time):
    for time in times:
        if time[0] == current_time:
            return time[1:len(time)]
    return None

# Send notes being activated or deactivated to arduino
def send_notes(arduino, notes):
    array_string = ','.join(map(str, notes))
    arduino.write(bytes(array_string + '\n', 'utf-8'))  # Add '\n' to indicate end of array
    data = arduino.readline().decode()
    return data

def main():
    if len(sys.argv) != 2:
        print("Usage: needs a midi file")
        sys.exit(1)
        
    midi_file_path = sys.argv[1]
    mid = remove_dups(midi_file_path)
    
    print(mid)
    
    
    ticks_per_beat = mid.ticks_per_beat
    
    arduino = serial.Serial(port='COM5', baudrate=31250, timeout=.1)
    time.sleep(2) # Give time for arduino to connect before sending info
    arduino.write(bytes('start' + '\n', 'utf-8'))
    data = arduino.readline().decode()
    print(data)
    tempo = 250000
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                print(tempo)
                break
        times, total_time = get_times(track)
        delay = 60000 / (ticks_per_beat * tempo)
        # delay = 0.0001
        print(delay)
        for i in range(total_time + 1):
            notes = contains_time(times, i)
            if notes is not None:
                print(notes)
                data = send_notes(arduino, notes)
            # Time should actually pass. This should be tweaked using tempo (i think)
            # Probably end up using some random value like how it is now
            time.sleep(delay)
        arduino.write(bytes('end' + '\n', 'utf-8'))
        data = arduino.readline().decode()
        print(data)
        break
    
#------------------------------------------------------------------
if __name__ == '__main__':
    main()

