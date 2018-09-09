from collections import defaultdict
from mido import MidiFile, tempo2bpm
from enum import Enum

import json

PhraseOwner = Enum('PhraseOwner', 'Team1 Team2 Both', module=__name__)

class Note():
	def __init__(self, start_time_ticks, end_time_ticks, midi_number, owner, ticks_per_beat=480.0, modulo=5):
		'''
		time_ticks: time in ticks
		midi_number: note number
		tempo=500000: microseconds per beat
		ticks_per_beat=480: ticks per beat. Provided that `ticks` are the default mid time format
		'''
		start_time_in_beats = start_time_ticks / ticks_per_beat
		end_time_in_beats = end_time_ticks / ticks_per_beat
		self._owner = owner
		self._midi_number = midi_number
		self._start_beat = start_time_in_beats
		self._end_beat = end_time_in_beats
		self._modulo = modulo

	def wrap_note(self):
		return self._midi_number % self._modulo

	@property
	def dict(self):
		return {'Owner': self._owner,
				'StringIndex': self.wrap_note(), 
		        'StartBeat': self._start_beat,
		        'EndBeat': self._end_beat}
	

class Track():
	def __init__(self, name='phrase_boss1', tempo=500000, ticks_per_beat=480, owner=None, string_index=0):
		self._name = name
		self._owner = owner
		self._notes = []
		self._string_index = string_index

	def _dispatch_enclosure(self, notes_starts, event):
			return notes_starts.pop(event.note, None)

	def parse_midi_events(self, mid_events, owner):
		self._notes = []
		notes_starts = {}
		current_time = 0
		for event in mid_events:
			if event.type is 'note_on':
				notes_starts[event.note] = event.time + current_time

			if event.type is 'note_off':
				note_start = self._dispatch_enclosure(notes_starts, event)
				if note_start is not None:
					new_note = Note(note_start, 
									current_time + event.time, 
									event.note, 
									owner)
					self._notes.append(new_note)
				else:
					print('found note without enclosure!', err)
					return
			try:		
				current_time += event.time

			except Exception as err:
				print('Only note-related events are supposed to hold the `time` property.')
				pass

	def get_monophonic_notes(self, owner):
		try:
			mono_notes = [self._notes[0].dict]
		except Exception:
			return None

		for note in self._notes:
			if note._start_beat != mono_notes[-1]['StartBeat']:
				mono_notes.append(note.dict)
		return mono_notes

	# def serialize_notes(self, owner, initial_notes_dict):
	# 	mono_notes_dict = self.get_monophonic_notes_dict(owner)
	# 	file_name = '%s%s.json' % (self._name, self._owner)
	# 	initial_notes_dict
	# 	with open(file_name, 'w') as f:
	# 		data_to_dump = {'StartBpm': 120, 
	# 						'Notes': mono_notes_dict}
	# 		json.dump(data_to_dump, f)

class Music():
	def __init__(self, tracks, name):
		self._name = name
		self._tracks = tracks

	def serialize_notes(self):
		file_name = '%s.json' % (self._name)
		with open(file_name, 'w') as f:
			mono_notes = []
			for owner, track in self._tracks.items():
				track_notes = track.get_monophonic_notes(owner)
				if track_notes is not None:
					mono_notes += track_notes

			data_to_dump = {'StartBpm': 120, 
							'Notes': mono_notes}
			json.dump(data_to_dump, f)	
		
def load_mid(file):
	mid = MidiFile(file)
	tracks = {}
	for i, track in enumerate(mid.tracks):

		tracks[i] = []
		for msg in track:
			tracks[i].append(msg)
	return tracks

def remove_control_msgs(tracks):
	for track in tracks.values():
		track = [event for event in track if event.type is not 'control_change']

	return tracks

def events_to_json(events):
	raise NotImplementedError()
