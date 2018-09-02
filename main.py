from midi_operations import *
import json

def main():
	raw_tracks = load_mid('test1.mid')
	raw_tracks = remove_control_msgs(raw_tracks)
	tracks = {}
	for key, track in raw_tracks.items():
		tracks[key] = Track(name=key)
		tracks[key].parse_midi_events(track)
		tracks[key].serialize_notes()
		# tracks[key] = tracks[key].get_monophonic_notes()




if __name__ == "__main__":
	main()    
