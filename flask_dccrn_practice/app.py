from flask import Flask

import torch
import json
import os

from wav2json import wav2json
from json2wav import json2wav

app = Flask(__name__)

model = torch.load('dccrn.pt').eval()
device = torch.device('cpu')

count = 0

@app.route("/")
def hello():
    return "Hello goorm!"

@app.route("/test")
def predict():
    if not os.path.exists('./processed_jsons'):
        os.makedirs('./processed_jsons')

    wav2json('./test/')
    for json_file in os.listdir('./jsons/'):
        if os.path.isfile(f"./waves/{json_file[:-5]}_processed.wav"):
            continue

        with open('./jsons/'+ json_file, "r") as file:
            wav_json_data = json.load(file)

        noisy = wav_json_data["instances"]
        noisy_tensor = torch.tensor([noisy]).to(device)
        clean_array = model(noisy_tensor).squeeze().detach().numpy()

        processed_data = json.dumps({"name": wav_json_data["name"] + '_processed',
                                     "instances": clean_array.tolist()})

        with open(f'./processed_jsons/{wav_json_data["name"]}_processed.json', "w") as file:
            file.write("%s" % processed_data)

    json2wav('./processed_jsons/')
    return "Finish processing"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
