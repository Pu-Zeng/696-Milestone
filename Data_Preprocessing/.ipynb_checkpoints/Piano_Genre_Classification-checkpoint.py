import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
import pretty_midi
import warnings
from scipy.ndimage import zoom
import pypianoroll
from pypianoroll import Multitrack, Track
import mido
import string
import pickle
import pypianoroll


def get_pianoroll_data(sample_data, seconds_per_row):
    music_data = []
    for row in tqdm(sample_data.iterrows()):
        # print(row[1].address + '/' + os.listdir(row[1].address)[0])
        try:
            multitrack = pypianoroll.read(row[1].address + '/' + os.listdir(row[1].address)[0])            
            channel = multitrack.stack().shape[0]
            height = int(multitrack.stack().shape[1]/multitrack.tempo[0][0]/multitrack.resolution*60/seconds_per_row)
            res = np.zeros([channel,height, 128])
            a = multitrack.stack()
            res = zoom(a, (1, height/a[0].shape[0], 1))
            program = [track.program for track in multitrack.tracks]
            music_data.append([row[1].genre_more, program, res.mean(axis=0)])
        except:
                pass
    return music_data


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='The directory of ADL_Piano')
    parser.add_argument('output_dir', help='The output directory')

    args = parser.parse_args()

    target_path=args.input_dir

    all_content=os.listdir(target_path)
    print('All content numbers is',len(all_content))
    res = []

    def dfs_showdir(path, depth, label):
        for item in os.listdir(path):
            # if '.git' not in item:
                newitem = path +'/'+ item
                if os.path.isdir(newitem):
                    dfs_showdir(newitem, depth +1, label+[item])
                else:
                    res.append([label, path])

    label = []

    dfs_showdir(target_path, 0, label)

    data = [[a[0][0], a[1]] for a in res]

    music = pd.DataFrame(data,columns = ['genre', 'address'])
    idx = list(music.groupby('genre').agg('count').sort_values(by = 'address', ascending=False).index)
    # music.groupby('genre').agg('count').sort_values(by = 'address', ascending=False)[:20]
    music.columns = ['genre_more','address']


    bins_ = np.linspace(0, len(music)+1, 10).astype(int)
    for n in range(1,len(bins_)):
        music_data = get_pianoroll_data(music.iloc[bins_[n-1]:bins_[n]], 0.1)
        file=open(args.output_dir + "/music_data"+str(n)+".bin","wb")
        pickle.dump(music_data,file) 
        file.close()    