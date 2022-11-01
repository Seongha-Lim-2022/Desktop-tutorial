from flask import Flask
from flask import request, jsonify

import torch
import json
import os
import librosa
import soundfile as sf
import requests
import time
import numpy as np

app = Flask(__name__)

model = torch.load('dccrn.pt').eval()
device = torch.device('cpu')

count = 0

@app.route("/")
def hello():
    return "Hello goorm!"


@app.route("/send_wav", methods=['GET'])
def send_wav():
    start = time.time()
    wav_folder_url = './test/'

    if wav_folder_url[-1] == '/':
        path = wav_folder_url
    else:
        path = wav_folder_url + '/'

    file_list = os.listdir(path)

    file_list_wav = [file for file in file_list if file.endswith(".wav") and
                     not os.path.isfile(f"./waves/{file[:-4]}_processed.wav")]

    if len(file_list_wav) == 0:

        return 'there are no files to process'

    else:
        test_data = dict({"time": start,
                          "wav_list": file_list_wav})
        res = requests.post("http://127.0.0.1:80/processed_wav", data=json.dumps(test_data))

        return f'{res.text}'




@app.route('/processed_wav', methods=['POST'])
def processed_wav():

    wav_data = json.loads(request.get_data())

    file_list_wav = wav_data["wav_list"]

    if not os.path.exists('./waves'):
        os.makedirs('./waves')

    result_str = ""

    for wav_file in file_list_wav:

        noisy, sr = librosa.load('./test/'+ wav_file, sr=16000)
        noisy_tensor = torch.tensor(np.array([noisy])).to(device)
        clean_array = model(noisy_tensor).squeeze().detach().numpy()

        wav_name = wav_file[:-4] + '_processed'
        wav_vec = clean_array.tolist()

        sf.write(f'./waves/{wav_name}.wav', wav_vec, 16000, format='wav')
        result_str += f"[Finish processing {wav_name[:-10]}.wav" + ", " + f"Processing time: {time.time() - wav_data['time']}]" + "\n"
        wav_data['time'] = time.time()

    return result_str

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)