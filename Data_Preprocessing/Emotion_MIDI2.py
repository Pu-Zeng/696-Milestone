import os
from tqdm import tqdm
from tqdm import tqdm
import re
import numpy as np
from scipy.ndimage import zoom
from langdetect import detect
import pretty_midi
import pickle
import pandas as pd

def dfs_showdir(path, depth, label):
    for item in os.listdir(path):
        # if '.git' not in item:
            newitem = path +'/'+ item
            if os.path.isdir(newitem):
                dfs_showdir(newitem, depth +1, label+[item])
            else:
                res.append([label[-1], path])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='The directory of Lakh')
    parser.add_argument('output_dir', help='The output directory')
    args = parser.parse_args()

    target_path=args.input_dir+'/'
    output_dir = args.output_dir+'/'
    all_content=os.listdir(target_path)
    print('All content numbers is',len(all_content))
    res = []
    label = []
    for content in tqdm(all_content):
        if os.path.isdir(target_path+content):
            all_sub_content=os.listdir(target_path+content)
            for subcontent in all_sub_content:
                dfs_showdir(target_path+content+'/'+subcontent, 0, label+[subcontent])
    # dfs_showdir(target_path, 0, label)

    data = pd.DataFrame(res, columns = ['music_ID', 'address'])

    seconds_per_row = 0.05
    r = []
    midi_tranformed=[]
    bins_ = np.linspace(0, len(data)+1, 10).astype(int)
    for n in range(1,len(bins_)):
        music_data1 = []
        data_bin = data.iloc[bins_[n-1]:bins_[n]]
        for m in tqdm(data_bin.iterrows()):
            # print(row[1].address + '/' + os.listdir(row[1].address)[0])
            try:
                    # print(pretty.lyrics)
                # print(m[1].address + '/' + os.listdir(m[1].address)[0])
                if m[1].music_ID not in midi_tranformed:
                    midi_tranformed.append(m[1].music_ID)
                    m = pretty_midi.PrettyMIDI(m[1].address + '/' + os.listdir(m[1].address)[0])

                    if m.lyrics!=[]:
                        lyrics = ''.join([x.text for x in m.lyrics if re.match('\w',x.text) and x.time!=0]).lower()
                        # print(lyrics)
                        # multitrack = pypianoroll.read(row[1].address + '/' + os.listdir(row[1].address)[0])
                        # channel = multitrack.stack().shape[0]
                        if detect(lyrics) == 'en' and len(lyrics)>100:
                            roll = np.zeros_like(m.get_piano_roll())
                            count = 0
                            for i in m.instruments:
                                if i.program<=7:
                                    s1 =  i.get_piano_roll().shape
                                    roll[:,:s1[1]] += i.get_piano_roll()
                                    count+=1
                            roll = (roll/count).T
                            if np.isnan(roll).sum() == 0:
                                height = int(roll.shape[0]/m.estimate_tempo()/m.resolution*60/seconds_per_row)
                                res = np.zeros([height, 128])
                                res = zoom(roll, (height/roll.shape[0], 1)).astype(int)
                                # program = [track.program for track in multitrack.tracks]
                                music_data1.append([res, lyrics])
                                # r.append(roll)
            except:
                pass
        file = open(args.output_dir + '/lakh_lyric'+str(n)+'.bin', 'wb')
        pickle.dump(music_data1, file)
        file.close()
        print('Total number of muisc {}'.format(str(len(midi_tranformed))))