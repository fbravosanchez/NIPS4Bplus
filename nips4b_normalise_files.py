# -*- coding: utf-8 -*-

"""
Created by Francisco Bravo Sanchez July 2021
This scripts normalises the NIPS4B dataset files to process with the 
modified SincNet code

NIPS4B wav files:
http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_TEST_WAV.tar.gz

Instructions
https://github.com/fbravosanchez/NIPS4Bplus#readme
"""

import sys
import os
import glob
import soundfile as sf
import numpy as np

#path to NIPS4B_BIRD wav files
wav_path=sys.argv[1]
#output path
output_path = sys.argv[2]

if not os.path.exists(output_path):
    os.makedirs(output_path )


for i in glob.glob(os.path.join(wav_path , '') + '*.wav'):
    dirname, wav_file = os.path.split(i)
    [signal, fs] = sf.read(i)
    signal = signal.astype(np.float64)
    # Signal normalization
    signal = signal/np.abs(np.max(signal))
    sf.write(os.path.join(output_path , '') + wav_file, signal, fs)

