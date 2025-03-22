import pyaudio
import json
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import wave

def get_audio_files(path):
    wf = wave.open("speech.wav", "rb")
    # with open(path, 'r') as file:
    #     wf = wave.open("audio.wav", "rb")

get_audio_files("speech.wav")

        

# Загружаем модель
model = Model("models/vosk-model-ru-0.42")
recognizer = KaldiRecognizer(model, 16000)

# recognizer = KaldiRecognizer(model, 16000, '["нпв", "ддт", "ЗБС", "КНБК", "СПО", "ГИС", "Обслуживание БУ"]')

# Инициализируем PyAudio
mic = pyaudio.PyAudio()

# 🔹 Шумоподавление перед записью
sr_recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("🔄 Подстройка под окружающий шум...")
    sr_recognizer.adjust_for_ambient_noise(source, duration=2)  # Калибровка по шуму

# Открываем поток для микрофона
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                  input=True, frames_per_buffer=4000)
stream.start_stream()

print("🎤 Говорите...")

# Цикл распознавания в реальном времени
while True:
    data = stream.read(4000, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result["text"]
        print("Вы сказали:", text)

        if "стоп" in text:
            print("⏹ Завершение работы")
            break  # Останавливаем программу

# Закрываем микрофон
stream.stop_stream()
stream.close()
mic.terminate()


