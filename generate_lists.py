# -*- coding: utf-8 -*-

"""
This script reads the csv annotations from NIPS4Bplus and the species list from
NIPS4B to generate list of train and test files and dictionary label files

The dictionary files list random train and test sets for three selections of
classes: "All Classes", "Bird Classes" and "Bird Species"

It generates two separate test and train file sets. One for "All Classes" and a 
different one "birds" for both "Bird Classes" and "Bird Species"

Please set directories below before running script
"""



import os
import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


#Set directories here
#path to NIPS4Bplus csv annotation files
csv_path = '/temporal_annotations_nips4b/'
#path to cut files generated in cut_train_files_by_tag
cut_files_path = 'cut_files/'
#output path for generated dictionary files
output_path = 'data_lists/'
#path to NIPS4B species list
sps_list_file = '/NIPS4B_BIRD_CHALLENGE_TRAIN_LABELS/nips4b_birdchallenge_espece_list.csv'


#collect csv label file list
lbl_files = pd.DataFrame(glob.glob(csv_path + '*.csv'))
lbl_files.columns = ['csv']
lbl_files['wav'] = 'nips4b_birds_trainfile' + lbl_files['csv'].str[-7:-4]

#read species list
sps_list = pd.read_csv(sps_list_file)


file_list = []

#process by csv file
for i, j in lbl_files.iterrows():

    #skip empty files
    try:
        k = pd.read_csv(j['csv'], header=None)
        tags = True
    except pd.io.common.EmptyDataError:
        tags = False

    #for each valid csv file process tags
    if tags:
        for l, m in k.iterrows():
            #exclude files less than 10ms
            if m[1] > 0.01:
                file_out = cut_files_path+str(j['wav'])+'_'+str(l)+'.wav'
                try:
                    type_out = sps_list.loc[sps_list['class name'] ==
                                            m[2]].type.values[0]
                    scient_out = (sps_list.loc[sps_list['class name'] ==
                                               m[2]].Scientific_name.values[0])
                except:
                    type_out = ''
                    scient_out = ''
                dict_out = dict(zip(['File', 'Type', 'Class', 'Scientific'],
                                    [file_out, type_out, m[2], scient_out]))
                file_list.append(dict_out)

file_list = pd.DataFrame(file_list)

#Process all classes
file_list_all_classes = file_list[file_list['Type'] != '']

#Randomly split into train and test
train_files, test_files = train_test_split(file_list_all_classes['File'], test_size=0.25)

# save train and test file lists
if not os.path.exists(output_path):
    os.makedirs(output_path)
test_files.to_csv(output_path + 'all_classes_test_files.scp',
                  index=False, header=False, encoding='utf-8')
train_files.to_csv(output_path + 'all_classes_train_files.scp',
                   index=False, header=False, encoding='utf-8')

#Generate label dictionary files for All Classes
unique_all_class = pd.DataFrame(file_list_all_classes['Class'].unique())
unique_all_class.reset_index(drop=False, inplace=True)
unique_all_class.columns = ['Value', 'Class']

merge_class = pd.merge(file_list_all_classes, unique_all_class, how='left', on=['Class'])
class_dict = dict(zip(merge_class.File, merge_class.Value))

np.save(output_path + 'all_classes_labels.npy', class_dict)


#Process bird files
#Select only bird type files
file_list_birds = file_list[file_list['Type'] == 'bird']

#Repeat a random split into train and test including only birds
train_files, test_files = train_test_split(file_list_birds['File'], test_size=0.25)

# save train and test file lists
test_files.to_csv(output_path + 'bird_test_files.scp',
                  index=False, header=False, encoding='utf-8')
train_files.to_csv(output_path + 'bird_train_files.scp',
                   index=False, header=False, encoding='utf-8')


#Generate label dictionary files for Class
unique_bird_class = pd.DataFrame(file_list_birds['Class'].unique())
unique_bird_class.reset_index(drop=False, inplace=True)
unique_bird_class.columns = ['Value', 'Class']

merge_class = pd.merge(file_list_birds, unique_bird_class, how='left', on=['Class'])
class_dict = dict(zip(merge_class.File, merge_class.Value))

np.save(output_path + 'bird_classes_labels.npy', class_dict)

#Generate label dictionary files for Species
unique_bird_sps = pd.DataFrame(file_list_birds['Scientific'].unique())
unique_bird_sps.reset_index(drop=False, inplace=True)
unique_bird_sps.columns = ['Value', 'Scientific']

merge_scient = pd.merge(file_list_birds, unique_bird_sps, how='left', on=['Scientific'])
scient_dict = dict(zip(merge_scient.File, merge_scient.Value))

np.save(output_path + 'bird_species_labels.npy', scient_dict)

#Summary of the number of classes
print('Number of classes')
print('All Classes:', len(unique_all_class))
print('Bird Classes:', len(unique_bird_class))
print('Bird Species:', len(unique_bird_sps))
