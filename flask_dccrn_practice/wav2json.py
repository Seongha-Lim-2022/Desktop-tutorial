import librosa
import os
import json

def wav2json(wav_folder_url):
    if not os.path.exists('./jsons'):
        os.makedirs('./jsons')

    if wav_folder_url[-1] == '/':
        path = wav_folder_url
    else:
        path = wav_folder_url + '/'

    file_list = os.listdir(path)

    file_list_wav = [file for file in file_list if file.endswith(".wav")]

    for wav_file in file_list_wav:
        if os.path.isfile(f"./jsons/{wav_file[:-4]}.json"):
            continue

        noisy, sr = librosa.load(path + wav_file, sr=16000)
        test_data = dict({"name": wav_file[:-4],
                          "instances": noisy.tolist()})

        with open(f"./jsons/{wav_file[:-4]}.json", "w") as file:
            json.dump(test_data, file)

    return