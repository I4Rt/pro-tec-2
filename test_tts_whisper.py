import whisper
import pyaudio
import wave
import numpy as np
import speech_recognition as sr
import torch

print(torch.cuda.is_available())
device = "cuda" if torch.cuda.is_available() else "cpu"


# Загружаем модель (можно выбрать tiny, base, small, medium, large)
model = whisper.load_model("medium").to(device)

# Настройки микрофона
RATE = 16000  # Частота дискретизации
CHUNK = 1024  # Размер блока записи

sr_recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("🔄 Подстройка под окружающий шум...")
    sr_recognizer.adjust_for_ambient_noise(source, duration=2)  # Калибровка по шуму

# Инициализируем PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                input=True, frames_per_buffer=CHUNK)
stream.start_stream()

print("🎤 Говорите... (скажите 'стоп' для завершения)")

frames = []
while True:
    data = stream.read(CHUNK)
    print('data', data)
    frames.append(data)

    # Преобразуем в массив numpy
    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    text = model.transcribe(audio_data, language='ru', fp16=False, verbose=True)['text']
    # text = whisper.transcribe(model, audio_data)["text"].lower()

    # mel = whisper.log_mel_spectrogram(audio_data).to(model.device)
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")

    print("Вы сказали:", text)
    if "стоп" in text:
        print("⏹ Завершение работы")
        break  # Останавливаем программу

    # # Проверяем, сказали ли "стоп"
    # if "стоп" in :
    #     print("⏹ Завершение работы")
    #     break

# Останавливаем и закрываем поток
stream.stop_stream()
stream.close()
p.terminate()

# Сохраняем в файл (опционально)
# with wave.open("output.wav", "wb") as wf:
#     wf.setnchannels(1)
#     wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))

# print("🎧 Распознавание речи...")
# result = model.transcribe("output.wav")
# print("Вы сказали:", result["text"])
