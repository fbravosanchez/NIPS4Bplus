# -*- coding: utf-8 -*-

"""
Created by Francisco Bravo Sanchez July 2021
This scripts reads the NIPS4B wav files and splits them according to the
csv annotations from NIPS4Bplus (Morfi V, Bas Y, Pamula H, Glotin H,
Stowell D. 2019. NIPS4Bplus: a richly annotated birdsong audio dataset.
PeerJ Comput. Sci. 5:e223 http://doi.org/10.7717/peerj-cs.223)

NIPS4B wav files:
http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_TEST_WAV.tar.gz

NIPS4Bplus annotations:
https://doi.org/10.6084/m9.figshare.6798548

Instructions
https://github.com/fbravosanchez/NIPS4Bplus#readme
"""

import sys
import os
import glob
import pandas as pd
import soundfile as sf
import numpy as np


#Set directories
#path to NIPS4B_BIRD wav files
wav_path = sys.argv[1]
#path to NIPS4Bplus csv annotation files
csv_path = sys.argv[2]
#output path for generated cut files
output_path = sys.argv[3]

if not os.path.exists(output_path):
    os.makedirs(output_path)


#read csv label file list
lbl_files = pd.DataFrame(glob.glob(os.path.join(csv_path , '')+ '*.csv'))
lbl_files.columns = ['csv']
lbl_files['wav'] = 'nips4b_birds_trainfile' + lbl_files['csv'].str[-7:-4]


#process by csv file
for i, j in lbl_files.iterrows():

    #skip empty files
    try:
        k = pd.read_csv(j['csv'], header=None)
        tags = True
    except pd.errors.EmptyDataError:
        tags = False

    #for each valid csv file process wavefile
    if tags:
        [signal, fs] = sf.read(os.path.join(wav_path , '') + j['wav'] + '.wav')
        signal = signal.astype(np.float64)

        # Signal normalization
        signal = signal/np.abs(np.max(signal))

        #cut signal according to tag
        for l, m in k.iterrows():
            beg_sig = int(m[0]*fs)
            end_sig = int((m[0]+m[1])*fs)
            signal_cut = signal[beg_sig:end_sig]

            # Save cut signal as a new wavefile
            file_out = os.path.join(output_path, '') + str(j['wav']) +'_'+ str(l) + '.wav'
            sf.write(file_out, signal_cut, fs)
