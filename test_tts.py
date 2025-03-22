import torch
# from TTS.api import TTS
import speech_recognition as sr
import os

# device = "cuda" if torch.cuda.is_available() else "cpu"

# print(TTS().list_models())

# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

speech_text = 'В глубинах нашего воображения таится мир, полный неизведанных чудес и удивительных приключений. Этот мир доступен каждому из нас, в тот момент, когда мы позволяем своему уму раскрыть свои крылья и унести нас в удивительные путешествия.'
recognizer = sr.Recognizer()


with sr.Microphone() as source2:
    print('silence please')
    recognizer.adjust_for_ambient_noise(source2, duration=2)
    while True:
        print('speak please')
        audio = recognizer.listen(source2)
        # with open('listened_audio.wav', 'wb') as file:
        #     file.write(audio.get_wav_data())
        try:
            print(f'распознавание google: ', recognizer.recognize_google(audio, language='ru-RU').lower())
            print(f'распознавание sphinx: ', recognizer.recognize_sphinx(audio, language="ru-RU").lower())
        except sr.exceptions.UnknownValueError as e:
            print('UnknownValueError', e, type(audio))
            continue
        # read_text = text.lower()
        # print('read_text: ', read_text)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
# wav = tts.tts(text=speech_text, speaker_wav="voice.wav", language="ru")
# Text to speech to a file

# print('final round')
# tts.tts_to_file(text=speech_text, speaker_wav="listened_audio.wav", language="ru", file_path="output.wav")
# os.system(f"start output.wav")
