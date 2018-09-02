from collections import defaultdict
from mido import MidiFile, tempo2bpm
from enum import Enum

import json

PhraseOwner = Enum('PhraseOwner', 'Team1 Team2 Both', module=__name__)

class Note():
	def __init__(self, start_time_ticks, end_time_ticks, mid_number, tempo=500000, ticks_per_beat=480):
		'''
		time_ticks: time in ticks
		mid_number: note number
		tempo=500000: microseconds per beat
		ticks_per_beat=480: ticks per beat. Provided that `ticks` are the default mid time format
		'''
		start_time_in_beats = (start_time_ticks / ticks_per_beat)
		end_time_in_beats = (end_time_ticks / ticks_per_beat)

		self._mid_number = mid_number
		self._start_beat = start_time_in_beats
		self._end_beat = end_time_in_beats


class Track():
	def __init__(self, name='phrase_boss1', tempo=500000, ticks_per_beat=480, owner=None):
		self._name = name
		self._owner = owner # I dont think owner makes sense here.
	    self._notes = []	    

	def _dispatch_enclosure(self, notes_starts, event):
			return notes_starts.pop(event.note, None):

	def parse_midi_events(self, mid_events):
		notes_starts = {}
		current_time = 0
		for event in mid_events:
			
			if event.type is 'note_on':
				notes_starts[event.note] = event.time + current_time

			if event.type is 'note_off':
				note_start = self._dispatch_enclosure(notes_starts, event)
				if note is not None:
					current_time += event.time
					new_note = Note(note_start, 
									current_time, 
									event.note)
					self._notes.append(new_note)
				else:
					print('found note without enclosure!', err)
					return


def load_mid(file):
	mid = MidiFile(file)
	events = {}
	for i, track in enumerate(mid.tracks):
		events[i] = []
		for msg in track:
			events[i].append(msg)
	return events

def remove_control_msgs(events):
	for track in events.keys():
		track = [event for event in track if event.type is not 'control_change']

	return events

def events_to_json(events):
	raise NotImplementedError()