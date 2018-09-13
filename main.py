from midi_operations import *
from mido import tempo2bpm
import argparse
import json

def _parse_args():
    parser = argparse.ArgumentParser(description='Dumps json files from midi files.')

    parser.add_argument(
        '--file',
        dest='midi_file',
        default='test1.midi',
        help='midi file path')

    parser.add_argument(
        '--key',
        dest='key',
        default='0',
        help='key of the music in accordance with the midi chart.')
    
    args = parser.parse_args()

    return args

def main():
	args = _parse_args()
	raw_tracks = load_mid(args.midi_file)
	raw_tracks = remove_control_msgs(raw_tracks)
	tracks = {}
	bpm = int(tempo2bpm(raw_tracks[0][0].tempo))

	for owner, track in raw_tracks.items():		
		try:
			if track[0].name == 'player1':
				tracks[owner] = Track(name=0)
				tracks[owner].parse_midi_events(track, 0)
			elif track[0].name == 'player2':
				tracks[owner] = Track(name=1)
				tracks[owner].parse_midi_events(track, 1)
			
		except:
			pass
		
	music = Music(tracks, args.midi_file.split('.')[0], bpm)
	music.serialize_notes()

if __name__ == "__main__":
	main()    
