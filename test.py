from mido import MidiFile

def load_mid(file):
	mid = MidiFile(file)
	notes = {}
	for i, track in enumerate(mid.tracks):
		notes[i] = []
		for msg in track:
			notes[i].append(msg)
	return notes

