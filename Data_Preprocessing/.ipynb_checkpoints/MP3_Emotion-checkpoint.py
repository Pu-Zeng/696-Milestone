import pandas as pd
import os


def process_data(input_dir, output_dir):
    files = os.listdir(input_dir+'/'+'clips_45sec/clips_45seconds/')
    info = pd.read_csv(input_dir+'/'+'annotations/songs_info.csv')
    info.file_name = info.file_name.str.replace('\t','')
    annotation = pd.read_csv(input_dir+'/'+'annotations/static_annotations.csv')
    import librosa
    import librosa.display
    from tqdm import tqdm
    res = []

    for i in tqdm(list(range(len(annotation)))):
        try:
            row = annotation.iloc[i]
            audio_path = input_dir+'/'+'clips_45sec/clips_45seconds/'+str(int(row.song_id)) + '.mp3'
            y, sr = librosa.load(audio_path)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
            res.append([mfccs, row.mean_arousal, row.mean_valence])
        except:
            pass
    import pickle
    file = open(output_dir+'/'+'mfcc_emotion_dataset','wb')
    pickle.dump(res,file)
    file.close()
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='The directory of ADL_Piano')
    parser.add_argument('output_dir', help='The output directory')
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    process_data(input_dir, output_dir)
    