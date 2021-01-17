import pretty_midi
import numpy as np
PITCH = {0:0.66, 1:0.70, 2:0.74, 3:0.78, 4:0.84, 5:0.89, 6:0.5, 7:0.53, 8:0.56, 9:0.59, 10:0.62, 11:0.66, 12:0.7, 13:0.74, 14:0.8, 15:0.84, 16:0.9, 17:0.95, 18:1, 19:1.05, 20:1.13, 21:1.18, 22:1.25, 23:1.33, 24:1.4, 25:1.5, 26:1.57, 27:1.67, 28:1.8, 29:1.9, 30:3, 31:1.05, 32:1.13, 33:1.18, 34:1.25, 35:1.33}

file = input("MIDI FILE PATH:")

midi_data = pretty_midi.PrettyMIDI(file)

second = midi_data.get_end_time()
print( "midi file size:", second, "seconds")
print( "bpm:", midi_data.estimate_tempo())

tp = []

with open("./note/data/note/functions/ontick.mcfunction", "w") as f:
	for instrument in midi_data.instruments:
		if not instrument.is_drum:
			time = instrument.get_onsets()
			i = 0
			for note in instrument.notes:
				tp.append([time[i], pretty_midi.note_number_to_name(note.pitch)])
				f.write(f"execute at @a run execute if score Timer SECOND matches {int(time[i]*20)} run playsound minecraft:block.note_block.harp master @a ~ ~ ~ 1 {PITCH[int(note.pitch) % 36]}\n")

				i += 1
