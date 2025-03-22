import pyaudio
import json
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import wave
import os
from pydub import AudioSegment

def convert_audio(filepath):
    """ Конвертирует аудио в WAV (16 kHz, 16 бит, моно) """
    audio = AudioSegment.from_file(filepath)
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(filepath, format="wav")
    return filepath

def create_recognizer():
    model = Model("vosk-model-ru-0.42")
    recognizer = KaldiRecognizer(model, 16000)
    return recognizer

def analize_audio(recognizer, wf):
    try:
        print('Расшифровка...')
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result["text"]
                return text
    except Exception as e:
        print('e', e)

def get_audio_files(folder_path, recognizer):
    for file_name in os.listdir(folder_path):
        if file_name[-4:] == '.wav':
            file_path = os.path.join(folder_path, file_name)
            wf = wave.open(file_path, "rb")
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                file_path = convert_audio(file_path)
                wf = wave.open(file_path, "rb")
                print('convert audio')
            print(file_path)
            text = analize_audio(recognizer, wf)
            print("Расшифровка: ", text)

recognizer = ''
recognizer = create_recognizer()
get_audio_files('.', recognizer)


        
        
    # with open(path, 'r') as file:
    #     wf = wave.open("audio.wav", "rb")

# get_audio_files(".")

        

# # Загружаем модель
# 
# 

# # recognizer = KaldiRecognizer(model, 16000, '["нпв", "ддт", "ЗБС", "КНБК", "СПО", "ГИС", "Обслуживание БУ"]')

# # Инициализируем PyAudio
# mic = pyaudio.PyAudio()

# # 🔹 Шумоподавление перед записью
# sr_recognizer = sr.Recognizer()
# with sr.Microphone() as source:
#     print("🔄 Подстройка под окружающий шум...")
#     sr_recognizer.adjust_for_ambient_noise(source, duration=2)  # Калибровка по шуму

# # Открываем поток для микрофона
# # stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, 
# #                   input=True, frames_per_buffer=4000)
# # stream.start_stream()

# print("🎤 Говорите...")

# # Цикл распознавания в реальном времени
# # while True:
#     # data = stream.read(4000, exception_on_overflow=False)

#     # if recognizer.AcceptWaveform(data):
#     #     result = json.loads(recognizer.Result())
#     #     text = result["text"]
#     #     print("Вы сказали:", text)

#     #     if "стоп" in text:
#     #         print("⏹ Завершение работы")
#     #         break  # Останавливаем программу

# # Закрываем микрофон
# # stream.stop_stream()
# # stream.close()
# # mic.terminate()


