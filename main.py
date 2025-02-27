import smstools as sms
import soundfile as sf  # Audio read/write
import sys
import os # File read/write
import argparse

smssamp_version: str = '0.1.0'
smssamp_help: str = '''Usage: python3 main.py --infile [in_file] --outfile [out_file]

Arguments:
in_file = Path to input file [ex. /path/to/input.wav]
out_file = Path to output file [ex. /path/to/output.wav]
'''

argp = argparse.ArgumentParser()
argp.add_argument('-i', '--infile', type=str)
argp.add_argument('-o', '--outfile', type=str)
# argp.add_argument('-p', '--pitch', type=str)
# argp.add_argument('-v', '--velocity', type=float)
# argp.add_argument('-f', '--flags', type=str)
# argp.add_argument('-O', '--offset', type=float)
# argp.add_argument('-l', '--length', type=float)
# argp.add_argument('-c', '--consonant', type=float)
# argp.add_argument('-C', '--cutoff', type=float)
# argp.add_argument('-V', '--volume', type=float)
# argp.add_argument('-m', '--modulation', type=int)
# argp.add_argument('-t', '--tempo', type=str)
# argp.add_argument('-P', '--pitchbend', type=str)

smssp = argp.parse_args()

in_file: str = smssp.infile

out_file: str = smssp.outfile

def Render():
    r = open(in_file, 'rb')
    
    with open(out_file, 'xb') as R:
        R.write(r.read())
    
    r.close()

    # copy it over to to a set location with a different wav file name.


def main():
    # try:
        # in_file first, then out_file

    # except:
        # print(f'SMS-samp {smssamp_version}\n\n{smssamp_help}')
    Render()

if __name__ == '__main__':
    main()