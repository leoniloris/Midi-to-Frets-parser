from mido import MidiFile
from enum import Enum

class PhraseOwner(Enum):
     Team1 = 1
     Team2 = 2
     Both = 3

def load_mid(file):
	mid = MidiFile(file)
	notes = {}
	for i, track in enumerate(mid.tracks):
		notes[i] = []
		for msg in track:
			notes[i].append(msg)
	return notes

def remove_control_msgs(notes):
	for track in notes.keys():
		track = [note for note in track if note.type is not 'control_change']

	return notes

	