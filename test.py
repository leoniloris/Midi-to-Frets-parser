from collections import defaultdict
from mido import MidiFile, tempo2bpm
from enum import Enum

import json

PhraseOwner = Enum('PhraseOwner', 'Team1 Team2 Both', module=__name__)

class Event(Enum):


class Note():
	def __init__(self, start_time_ticks, end_time_ticks, mid_number, previous_event_beat, tempo=500000, ticks_per_beat=480):
		'''
		time_ticks: time in ticks
		mid_number: note number
		tempo=500000: microseconds per beat
		previous_event_beat: beat counter of the last event preceding the current note
		ticks_per_beat=480: ticks per beat. Provided that `ticks` are the default mid time format
		'''
		start_time_in_beats = (start_time_ticks / ticks_per_beat)
		end_time_in_beats = (end_time_ticks / ticks_per_beat)

		self._mid_number = mid_number
		self._start_beat = previous_event_beat + start_time_in_beats
		self._end_beat = self._start_beat + end_time_in_beats


class Track():
	def __init__(self, start_bpm, owner, name='phrase_boss1', tempo=500000, ticks_per_beat=480):
		self._start_bpm = start_bpm
		self._name = name
		self._owner = owner
	    self._notes = []	    

		self._start_bpm = start_bpm
		self._start_bpm = start_bpm

	def _dispatch_enclosure(self, notes_needing_enclosure, event):
		try:
			notes_needing_enclosure[event.note]
			return True
		except Exception as err:
			print('found note withoud enclosure!', err)
			return False


	def parse_midi_events(self, mid_events):
		notes_needing_enclosure = {}

		for event in mid_events:
			if event.type is 'note_on':
				notes_needing_enclosure[event.note] = {'start_time': event.time, 'end_time': None}

			if event.type is 'note_off':
				if self._dispatch_enclosure(notes_needing_enclosure, event):

				self._notes.append()

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
