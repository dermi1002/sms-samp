import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
import sys
import os
import pyworld as world # Vocoder
import smstools as sms # Main Vocoder
import numpy as np
from numba import njit, vectorize, float64, optional # JIT compilation stuff (and ufuncs)
import soundfile as sf # WAV read + write
import scipy.signal as signal # for filtering
import scipy.interpolate as interp # Interpolator for feats
import scipy.ndimage as ndimage
import resampy # Resampler (as in sampling rate stuff)
from pathlib import Path # path manipulation
import re

smssamp_version: str = '0.1.0'
smssamp_help: str = '''Usage: python3 sms-samp.py --infile [in_file] --outfile [out_file]

Arguments:
in_file = Path to input file [ex. /path/to/input.wav]
out_file = Path to output file [ex. /path/to/output.wav]
'''

notes = {'C' : 0, 'C#' : 1, 'D' : 2, 'D#' : 3, 'E' : 4, 'F' : 5, 'F#' : 6, 'G' : 7, 'G#' : 8, 'A' : 9, 'A#' : 10, 'B' : 11} # Note names lol
note_re = re.compile(r'([A-G]#?)(-?\d+)') # Note Regex for conversion
default_fs = 44100 # UTAU only really likes 44.1khz
fft_size = world.get_cheaptrick_fft_size(default_fs, world.default_f0_floor) # It's just 2048 but you know
cache_ext = '.sc.npz' # cache file extension

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