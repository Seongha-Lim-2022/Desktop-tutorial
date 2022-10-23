import soundfile as sf
import os
import json

def json2wav(json_folder_url):
    if not os.path.exists('./waves'):
        os.makedirs('./waves')

    if json_folder_url[-1] == '/':
        path = json_folder_url
    else:
        path = json_folder_url + '/'

    file_list = os.listdir(path)

    file_list_json = [file for file in file_list if file.endswith("_processed.json")]

    for json_file in file_list_json:
        if os.path.isfile(f"./waves/{json_file[:-5]}.wav"):
            continue

        with open(path + json_file, "r") as file:
            json_sample = json.load(file)

        wav_name = json_sample['name']
        wav_vec = json_sample['instances']

        sf.write(f'./waves/{wav_name}.wav', wav_vec, 16000, format='wav')

    return