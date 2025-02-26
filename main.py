import smstools as sms
import soundfile as sf  # Audio read/write
import sys
import os # File read/write

smssamp_version: str = '0.1.0'
smssamp_help: str = '''Usage: main.py [in_file] [out_file]

Arguments:
in_file = Path to input file [ex. /path/to/input.wav]
out_file = Path to output file [ex. /path/to/output.wav]
'''

def main():
    print(f'SMS-samp {smssamp_version}\n\n{smssamp_help}')

if __name__ == '__main__':
    main()