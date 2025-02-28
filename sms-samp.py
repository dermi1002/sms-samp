import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
import sys
import os
# import pyworld as world # Vocoder
import smstools # Main Vocoder
import numpy as np
from numba import njit, vectorize, float64, optional # JIT compilation stuff (and ufuncs)
import soundfile as sf # WAV read + write
import scipy.signal as signal # for filtering
import scipy.interpolate as interp # Interpolator for feats
import scipy.ndimage as ndimage
import resampy # Resampler (as in sampling rate stuff)
from pathlib import Path # path manipulation
import re
import argparse
# from signal import get_window
from smstools.models import hpsModel as HPS
from smstools.transformations import hpsTransformations as HPST
from smstools.transformations import harmonicTransformations as HT
from smstools.models import utilFunctions as UF

smssamp_version: str = '0.1.0'
smssamp_help: str = '''Usage: sms-samp in_file out_file pitch velocity [flags] [offset] [length] [consonant] [cutoff] [volume] [modulation] [tempo] [pitch_string]

Arguments:
in_file = Path to input file [ex. /path/to/input.wav]
out_file = Path to output file [ex. /path/to/output.wav]
'''

notes = {'C' : 0, 'C#' : 1, 'D' : 2, 'D#' : 3, 'E' : 4, 'F' : 5, 'F#' : 6, 'G' : 7, 'G#' : 8, 'A' : 9, 'A#' : 10, 'B' : 11} # Note names
note_re = re.compile(r'([A-G]#?)(-?\d+)') # Note Regex for conversion
default_fs = 44100 # UTAU only really likes 44.1khz
fft = 2048
cache_ext = '.sc.npz' # cache file extension

minf0 = 140
maxf0 = 1760

# Flags
flags = ['g', 'B', 'G', 'P']
flag_re = '|'.join(flags)
flag_re = f'({flag_re})([+-]?\\d+)?'
flag_re = re.compile(flag_re)

# WAV read/write
def read_wav(loc):
    """Read audio files supported by soundfile and resample to 44.1kHz if needed. Mixes down to mono if needed.

    Parameters
    ----------
    loc : str or file
        Input audio file.

    Returns
    -------
    ndarray
        Data read from WAV file remapped to [-1, 1] and in 44.1kHz
    """
    if type(loc) == str: # make sure input is Path
        loc = Path(loc)

    exists = loc.exists()
    if not exists: # check for alternative files
        for ext in sf.available_formats().keys():
            loc = loc.with_suffix('.' + ext.lower())
            exists = loc.exists()
            if exists:
                break

    if not exists:
        raise FileNotFoundError("No supported audio file was found.")
    
    x, fs = sf.read(loc)
    if len(x.shape) == 2:
        # Average all channels... Probably not too good for formats bigger than stereo
        x = np.mean(x, axis=1)

    if fs != default_fs:
        x = resampy.resample(x, fs, default_fs)

    return x

def save_wav(loc, x):
    """Save data into a WAV file.

    Parameters
    ----------
    loc : str or file
        Output WAV file.

    x : ndarray
        Audio data in 44.1kHz within [-1, 1].

    Returns
    -------
    None
    """
    sf.write(loc, x, default_fs, 'PCM_16')

#argp = argparse.ArgumentParser()
#argp.add_argument('-i', '--infile', type=str)
#argp.add_argument('-o', '--outfile', type=str)
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

#smssp = argp.parse_args()

#in_file: str = smssp.infile

#out_file: str = smssp.outfile

#def Render():
#    r = open(in_file, 'rb')
#    
#    with open(out_file, 'xb') as R:
#        R.write(r.read())
#    
#    r.close()

    # copy it over to to a set location with a different wav file name.


if __name__ == '__main__':
    logging.info(f'SMS-samp {smssamp_version}')
    print(f'HPS Args:\n{dir(smstools.models.hpsModel)}\n\nUtilFuntion Args:\n{dir(smstools.models.utilFunctions)}\n\nHPSTransformation Args:\n{dir(smstools.transformations.hpsTransformations)}\n\nHarmonic Args:\n{dir(smstools.transformations.harmonicTransformations)}')