## Information of folders

**test_original** : keyboard.wav, keyboard_processed.wav 존재.

**test** : keyboard.wav 파일과 복제본인 keyboard2.wav, keyboard3.wav 존재.

~~**jsons** : test 폴더의 wav 파일을 json 파일로 변환하여 저장. 이름은 원래 wav 파일의 이름과 동일.~~

~~**processed_jsons** : 소음을 제거한 상태의 json 파일을 저장. 이 때 이름은 json 파일 이름에 '_processed' 를 추가한 형태.~~

**waves** : processed_jsons 폴더의 json 파일을 wav 파일로 변환하여 저장. 이름은 원래 json 파일의 이름과 동일.


## main.py (2022.11.01.)

requests.post, request.get_data 이용

"/send_wav" 로 접속하여 소음 제거

1. test 폴더의 wav 파일을 불러온다.
2. 해당 wav 파일의 소음을 제거하여 waves 폴더에 wav 파일로 저장한다.
3. test 폴더의 모든 wav 파일의 소음을 제거, 각 파일 별 변환 시간을 같이 표시.
4. 변환할 wav 파일이 없으면 'there are no files to process' 출력



## app.py (2022.10.23.)

wav2json.py, json2wav.py 이용하여 구현. "/test"로 접속하면 test 폴더의 모든 wav 파일의 소음을 제거.

1. test 폴더의 wav 파일을 불러온다.
2. 해당 wav 파일을 json 파일로 변환하여 jsons 폴더에 저장한다.
3. jsons 폴더의 json 파일을 소음 제거하여 processed_jsons 폴더에 json 파일로 저장한다.
4. processed_json 폴더의 json 파일을 wav 파일로 변환하여 waves 폴더에 저장한다.


