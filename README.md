# SincNet vs NIPS4Bplus 

This repository contains scripts to replicate the experiments in [*Bioacoustic classification of avian calls from raw sound waveforms with an open source deep learning architecture*](https://www.nature.com/articles/s41598-021-95076-6). Part I describes the experiment with default settings, while Part II uses modified code to apply enhanced settings.

## Part I - Scripts to cut files and generate lists according to tags from NIPS4Bplus and instructions to run the SincNet experiment with default settings

[NIPS4Bplus](http://doi.org/10.7717/peerj-cs.223) provides detailed tags for the training dataset of the [2013 Neural
Information Processing Scaled for Bioacoustics (NIPS4B) challenge for bird song
classification](http://sabiod.lis-lab.fr/nips4b/challenge1.html). To use the data in [SincNet](http://arxiv.org/abs/1808.00158) with the default settings, we first prepare the files by cutting them according to the tags and then generate train, test and label lists. 
### 1 NIPS4Bplus data preparation.
#### a) Cut files
The first step is to cut the original training [NIPS4B wavefiles](https://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_TEST_WAV.tar.gz) according to the [NIPS4Bplus csv annotations](https://doi.org/10.6084/m9.figshare.6798548). Run the script *cut_nips4bplus_files.py* as follows:

```
python cut_nips4bplus_files.py nips4b_bird_wav_folder nips4bplus_csv_folder output_path
```

where:

+ *nips4b_bird_wav_folder* is the folder with the original training NIPS4B wavefiles
+ *nips4bplus_csv_folder* is the folder with the NIPS4Bplus csv annotation files
+ *output_path* is the output path for the cut files

This generates new (short) wavefiles from the tag dimensions and stores them in the output_path.

#### b) Generate lists

Then we generate lists of files and labels running *generate_file_lists.py* with:

```
pyton generate_file_lists.py nips4bplus_csv_folder nips4b_birdchallenge_espece_list.csv output_path
```

where:

+ *nips4bplus_csv_folder* is the folder with the NIPS4Bplus csv annotation files
+ *nips4b_birdchallenge_espece_list.csv* is the NIPS4B species list (csv) within the [NIPS4B train labels](http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_LABELS.tar)
+ *output_path* is the output path for the lists of files and labels

This generates lists of train and test files, and dictionary label files. The dictionary files list three class selections: *All Classes*, *Bird Classes* and *Bird Species*. But, there are only two sets of random train and test files: *all_classes* and *bird*. The set *bird* is combined with both the *Bird Classes* and *Bird Species* dictionaries for the respective experiments. Samples of these files are included under [data_lists](https://github.com/fbravosanchez/NIPS4Bplus/tree/master/data_lists)

### 2 Run the SincNet experiment with default settings
Use the SincNet code from:
https://github.com/mravanelli/SincNet. Follow the instructions in the SincNet repository but instead of using the Timit experiment settings, use one of the [cfg](https://github.com/fbravosanchez/NIPS4Bplus/tree/master/cfg) files corresponding to your choice of experiment to run: *all classes*, *bird classes* or *bird species*. The [cfg](https://github.com/fbravosanchez/NIPS4Bplus/tree/master/cfg) files maintain the settings of the Timit experiment in the [SincNet repository](https://github.com/mravanelli/SincNet) except for the [changes required](https://www.nature.com/articles/s41598-021-95076-6) for this dataset and each individual experiment. Modify the [data] section of the corresponding cfg file (ie. [*cfg/nips4bplus_all_classes.cfg*](https://github.com/fbravosanchez/NIPS4Bplus/tree/master/cfg/nips4bplus_all_classes.cfg)) according to your paths.

+ *tr_lst* is the *"all_classes_train_files.scp"* generated in b) above
+ *te_lst* is the *"all_classes_test_files.scp"* generated in b) above
+ *lab_dict* is the *"all_classes_labels.npy"* generated in b) above
+ *data_folder* is the folder with the cut files generated in a) above
+ *output_path* is the output path for the training results and model files

Then run *speaker_id.py* from [SincNet](https://github.com/mravanelli/SincNet) as follows:

```
python speaker_id.py -–cfg=cfg/nips4bplus_all_classes.cfg
```

You may need to modify *"cfg/nips4bplus_all_classes.cfg"* according to your path and choice of experiment. Note that you would need *data_io.py* and *dnn_models.py* from [SincNet](https://github.com/mravanelli/SincNet) in the same directory.

## Part II - Running enhanced SincNet models with modified SincNet code

In order to process NIPS4Bplus tagged calls that are shorter than the frame length (cw_len) we have modified the SincNet code. The code utilises the original whole NIPS4B training files, but they need prior normalisation. 

### 1 Normalise NIPS4B files

Run the code to normalise the original training [NIPS4B wavefiles](http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_TEST_WAV.tar.gz) as follows:
```
python nips4b_normalise_files.py nips4b_bird_wav_folder output_folder
```

where:
+ *nips4b_bird_wav_folder* is the folder of the original training NIPS4B wavefiles
+ *output_folder* is the output folder for the normalised files

### 2 Generate lists

Generate csv lists of files acording to the [NIPS4Bplus csv annotations](https://doi.org/10.6084/m9.figshare.6798548) running *generate_mod_file_lists.py* with:

```
pyton generate_mod_file_lists.py nips4bplus_csv_folder nips4b_birdchallenge_espece_list.csv output_path
```

where:

+ *nips4bplus_csv_folder* is the folder with the NIPS4Bplus csv annotation files
+ *nips4b_birdchallenge_espece_list.csv* is the NIPS4B species list (csv) within the [NIPS4B train labels](http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_LABELS.tar)
+ *output_path* is the output path for the lists of files and labels

This generates random train and test lists (that include the tag labels) as csv files for three selections of classes: *All Classes*, *Bird Classes* and *Bird Species*. Samples of these csv files are included under [mod_data_lists](https://github.com/fbravosanchez/NIPS4Bplus/tree/master/mod_data_lists).

### 3 Run the modified SincNet code

The script *call_id.py* is a modified version of the *speaker_id.py* script from [SincNet](https://github.com/mravanelli/SincNet). First modify the [data] section, according to your paths, of one of the [mod_cfg](https://github.com/fbravosanchez/NIPS4Bplus/tree/master/mod_cfg) files corresponding to your choice of experiment to run: *all classes*, *bird classes* or *bird species* (ie. *mod_cfg/mod_nips4bplus_all_classes.cfg*).

+ *tr_lst* is the *"mod_all_classes_train_files.csv"* generated in step 2 above
+ *te_lst* is the *"mod_all_classes_test_files.csv"* generated in step 2 above
+ *lab_dict* is not needed
+ *data_folder* is the folder with the normalised files generated in step 1 above
+ *output_path* is the output path for the training results and model files

Each [mod_cfg](https://github.com/fbravosanchez/NIPS4Bplus/tree/master/mod_cfg) file includes the best settings that we found for each experiment.

Then run *call_id.py* as follows:

```
python call_id.py --cfg=mod_cfg/mod_nips4bplus_all_classes.cfg
```

You may need to modify *"mod_cfg/mod_nips4bplus_all_classes.cfg"* according to your path and choice of experiment. Note that you would need *data_io.py* and *dnn_models.py* from [SincNet](https://github.com/mravanelli/SincNet) in the same directory.


## Requirements
The requirements of the code are those of SincNet (https://github.com/mravanelli/SincNet#prerequisites) as well as the libraries [glob](https://docs.python.org/library/glob.html), [pandas](https://pandas.pydata.org) and [sklearn](https://scikit-learn.org).

## Acknowledgements

We would like to acknowledge the authors of [NIPS4Bplus](http://doi.org/10.7717/peerj-cs.223) and [SincNet](https://arxiv.org/abs/1808.00158), and their contribution to open science.

## References and Sources

Bravo Sanchez, F., Hossain, R., English, N., Moore, S. *Bioacoustic classification of avian calls from raw sound waveforms with an open-source deep learning architecture*. Sci Rep (2021)
https://www.nature.com/articles/s41598-021-95076-6

Morfi, V., Bas, Y., Pamuła, H., Glotin, H. & Stowell, D. *NIPS4Bplus: a richly annotated birdsong audio dataset*. PeerJ Computer Science 5, e223 (2019).
http://doi.org/10.7717/peerj-cs.223

Ravanelli, M. & Bengio, Y. *Speaker Recognition from Raw Waveform with SincNet*. in 2018 IEEE Spoken Language Technology Workshop (SLT) 1021–1028 (IEEE, 2018).
https://arxiv.org/abs/1808.00158

Source of NIPS4B train labels
http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_LABELS.tar

Source of NIPS4B wav files:
http://sabiod.univ-tln.fr/nips4b/media/birds/NIPS4B_BIRD_CHALLENGE_TRAIN_TEST_WAV.tar.gz

Source of NIPS4Bplus transcriptions:
https://doi.org/10.6084/m9.figshare.6798548
