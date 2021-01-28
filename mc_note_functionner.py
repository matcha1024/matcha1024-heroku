from flask import Flask, request, redirect, url_for, send_file, render_template
import pretty_midi
import shutil

def create_function(): 

    PITCH = {0:0.67, 1:0.710, 2:0.714, 3:0.718, 4:0.84, 5:0.89, 6:0.5, 7:0.53, 8:0.56, 9:0.59, 10:0.63, 11:0.67, 12:0.71, 13:0.714, 14:0.79, 15:0.84, 16:0.9, 17:0.95, 18:1, 19:1.05, 20:1.13, 21:1.18, 22:1.25, 23:1.33, 24:1.4, 25:1.5, 26:1.57, 27:1.67, 28:1.8, 29:1.9, 30:2, 31:1.05, 32:1.13, 33:1.18, 34:1.25, 35:1.33}

    midi_data = pretty_midi.PrettyMIDI("./midi_file.mid")
    end_time = midi_data.get_end_time()

    with open("./note/data/note/functions/ontick.mcfunction", "w") as f:
        f.write(f"scoreboard players add Timer TICK 1\nscoreboard players operation Timer TICK %= Timer 20\nexecute if score Timer TICK matches 0 unless score Timer SECOND matches -1 run scoreboard players add Timer SECOND 1\nexecute if score Timer LOOP matches 1 if score Timer SECOND matches {int(end_time * 20)} run function note:start\n")
        for instrument in midi_data.instruments:
            if not instrument.is_drum:
                time = instrument.get_onsets()
                i = 0
                for note in instrument.notes:
                    f.write(f"execute at @a run execute if score Timer SECOND matches {int(time[i]*20)} run playsound minecraft:block.note_block.harp master @a ~ ~ ~ 1 {PITCH[int(note.pitch) % 36]}\n")

                    i += 1


    shutil.make_archive("note", "zip", root_dir = "./note")
