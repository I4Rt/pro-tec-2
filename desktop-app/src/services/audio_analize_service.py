import json
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import wave
import os
from pydub import AudioSegment
import time
from src.dto.base_dto import *
import re


class AudioAnalizeService:

    def __init__(self):
        self.frame_rate = 16000
        self.sample_width = 2
        self.channels = 1
        self.read_framerates = 4000

        # self.recognizer = self.create_recognizer() # with vosk
        self.recognizer = sr.Recognizer() # with google

        self.keywords = ['время начала', 'время начало', 'время окончания', 'забой', 'забои', 'за бой', 'этап', 'комментарий']

    def get_next_elem(self, keyword_index):
        return self.parts[keyword_index]
        # index = self.parts.index(self.keywords[keyword_index])
        # value = self.parts[index + 1] if index + 1 < len(self.parts) else ''
        # return value

    def return_table_data(self, raw_text:str, file_path):
        pattern = r'\b(' + '|'.join(map(re.escape, self.keywords)) + r')\b'
        raw_text = raw_text.replace('.', '')
        parts = re.split(pattern, raw_text)
        self.parts = [part.strip() for part in parts if part.strip()]

        markup_dto = MarkdownDTO(
            markup_id=str(int(time.time() * 100)),
            start_time=self.get_next_elem(1),
            end_time=self.get_next_elem(3),
            deep=self.get_next_elem(5),
            step=self.get_next_elem(7),
            comment=self.get_next_elem(9), 
            audio_path=file_path,
            raw_text=raw_text
        )
        return markup_dto

    def create_recognizer(self):
        try:
            model = Model(r"models\vosk-model-ru-0.42")
            recognizer = KaldiRecognizer(model, self.frame_rate)
            return recognizer
        except Exception as e:
            print('create_recognizer error', e)

    def convert_audio(self, filepath):
        """ Конвертирует аудио в WAV (16 kHz, 16 бит, моно) """
        audio = AudioSegment.from_file(filepath)
        audio = audio.set_channels(self.channels).set_frame_rate(self.frame_rate).set_sample_width(self.sample_width)
        audio.export(filepath, format="wav")
        return filepath

    def analize_audio(self, wf):
        try:
            print('Расшифровка...')
            while True:
                data = wf.readframes(self.read_framerates)
                if len(data) == 0:
                    break
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result["text"]
                    return text
        except Exception as e:
            print('e', e)

    def recognize_audio_from_file(self, audio_file):
        with sr.AudioFile(audio_file) as source:
            print("Распознавание текста...")
            audio = self.recognizer.record(source)  # Читаем весь файл
            try:
                text = self.recognizer.recognize_google(audio, language='ru-RU')
                return text
            except sr.UnknownValueError:
                print("Не удалось распознать текст.")
            except sr.RequestError as e:
                print(f"Ошибка сервиса распознавания: {e}")

    def get_audio(self, file_path):
        wf = wave.open(file_path, "rb")
        if wf.getnchannels() != self.channels or wf.getsampwidth() != self.sample_width or wf.getframerate() != self.frame_rate:
            file_path = self.convert_audio(file_path)
            time.sleep(2)
            wf = wave.open(file_path, "rb")
            print('convert audio')
        print(file_path)
        # text = self.analize_audio(wf) # with vosk
        text = self.recognize_audio_from_file(file_path) # with google
        print("Расшифровка: ", text)
        return self.return_table_data(text, file_path)
        

    def get_audio_files(self, folder_path):
        for file_name in os.listdir(folder_path):
            if file_name[-4:] == '.wav':
                file_path = os.path.join(folder_path, file_name)
                return self.get_audio(file_path)
    
                