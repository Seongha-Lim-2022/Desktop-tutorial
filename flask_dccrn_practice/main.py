from flask import Flask
from flask import request, jsonify

import torch
import json
import os
import librosa
import soundfile as sf
import requests

app = Flask(__name__)

model = torch.load('dccrn.pt').eval()
device = torch.device('cpu')

count = 0

@app.route("/")
def hello():
    return "Hello goorm!"


@app.route("/send_wav", methods=['GET'])
def send_wav():
    wav_folder_url = './test/'
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

        res = requests.post("http://127.0.0.1:80/processed_wav", data=json.dumps(test_data))
        return res.text

    return 'there are no files to process'


@app.route('/processed_wav', methods=['POST'])
def processed_wav():
    if not os.path.exists('./processed_jsons'):
        os.makedirs('./processed_jsons')

    wav_json_data = json.loads(request.get_data())
    if len(wav_json_data) == 0:
        return 'No parameter'

    noisy = wav_json_data["instances"]
    noisy_tensor = torch.tensor([noisy]).to(device)
    clean_array = model(noisy_tensor).squeeze().detach().numpy()

    processed_data = {"name": wav_json_data["name"] + '_processed',
                                 "instances": clean_array.tolist()}

    json_sample = json.dumps(processed_data)

    with open(f'./processed_jsons/{wav_json_data["name"]}_processed.json', "w") as file:
        file.write("%s" % json_sample)

    if not os.path.exists('./waves'):
        os.makedirs('./waves')

    if not os.path.isfile(f"./waves/{processed_data['name']}.wav"):
        wav_name = processed_data['name']
        wav_vec = processed_data['instances']

        sf.write(f'./waves/{wav_name}.wav', wav_vec, 16000, format='wav')

    return f"Finish processing {wav_name[:-10]}.wav"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)