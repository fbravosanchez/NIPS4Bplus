# NIPS4Bplus

Scripts to cut files and generate list according to tags from NIPS4Bplus (Morfi V, Bas Y, Pamula H, Glotin H, Stowell D. 2019. NIPS4Bplus: a richly annotated birdsong audio dataset.
PeerJ Comput. Sci. 5:e223 http://doi.org/10.7717/peerj-cs.223)



cut_files.py reads the NIPS4B wav files and splits them according to the
csv annotations 

Source of NIPS4B wav files:
http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_TEST_WAV.tar.gz

Source of NIPS4Bplus transcriptions:
https://doi.org/10.6084/m9.figshare.6798548



generate_lists.py reads the csv annotations from NIPS4Bplus and the species list from
NIPS4B to generate list of train and test files and dictionary label files

The dictionary files list random train and test sets for three selections of
classes: "All Classes", "Bird Classes" and "Bird Species"

It generates two separate test and train file sets. One for "All Classes" and a 
different one "birds" for both "Bird Classes" and "Bird Species"

Please set directories in the scripts before running
