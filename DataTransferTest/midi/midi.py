import rtmidi
import mido
import cv2

print("MIDI output ports: ", mido.get_output_names())
midiOutput = mido.open_output("2- LoopBe Internal MIDI 1")


def sendNoteOn(note, velocity):
	message = mido.Message('note_on', note=note, velocity=velocity)
	midiOutput.send(message)

def sendNoteOff(note, velocity):
	message = mido.Message('note_off', note=note, velocity=velocity)
	midiOutput.send(message)


for value in range(128):
	sendControlchange(7, value)
	cv2.waitKey(500)