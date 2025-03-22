import wave
import speech_recognition as sr
import pyaudio

def record_audio_to_file(output_file):
    # Настройки записи
    chunk = 1024  # Размер блока
    format = pyaudio.paInt16  # Формат записи
    channels = 1  # Количество каналов (моно)
    rate = 16000  # Частота дискретизации

    sr_recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🔄 Подстройка под окружающий шум...")
        sr_recognizer.adjust_for_ambient_noise(source, duration=2)  # Калибровка по шуму

    # Инициализация PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    print("🎤 Запись началась. Нажмите Ctrl+C для завершения...")
    frames = []

    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print("⏹ Запись завершена.")
    finally:
        # Останавливаем и закрываем поток
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Сохраняем аудио в файл
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        print(f"✅ Аудио сохранено в файл: {output_file}")

def recognize_audio_from_file(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        print("🎧 Распознавание текста...")
        audio = recognizer.record(source)  # Читаем весь файл
        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            print("📝 Распознанный текст:", text)
        except sr.UnknownValueError:
            print("❌ Не удалось распознать текст.")
        except sr.RequestError as e:
            print(f"❌ Ошибка сервиса распознавания: {e}")

if __name__ == "__main__":
    audio_file = "recorded_audio.wav"
    record_audio_to_file(audio_file)  # Записываем аудио
    recognize_audio_from_file(audio_file)  # Распознаем текст из записанного файла