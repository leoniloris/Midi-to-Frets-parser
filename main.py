from midi_operations import *
import argparse
import json

def _parse_args():
    parser = argparse.ArgumentParser(description='Dumps json files from midi files.')

    parser.add_argument(
        '--file',
        dest='midi_file',
        default='test1.midi',
        help='midi file path')
    args = parser.parse_args()

    return args

def main():
	args = _parse_args()
	raw_tracks = load_mid(args.midi_file)
	raw_tracks = remove_control_msgs(raw_tracks)
	tracks = {}
	for key, track in raw_tracks.items():
		tracks[key] = Track(name=key)
		tracks[key].parse_midi_events(track)
		tracks[key].serialize_notes()

if __name__ == "__main__":
	main()    
