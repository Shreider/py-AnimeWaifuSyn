import keyboard
import pyaudio
import wave
import time
import openai
import asyncio
from voicevox import Client
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pydub.playback import play
import psutil
import subprocess

file_name = "recording.wav"
openai_key = "api_key"

openai.api_key = openai_key

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

def playAudio():
    audio_file = AudioSegment.from_file("voice.wav", format="wav")
    play(audio_file)

async def speech(text):
    async with Client() as client:
        audio_query = await client.create_audio_query(text, speaker=10)
        with open("voice.wav", "wb") as f:
            f.write(await audio_query.synthesis())
    playAudio()

def translate(text):
    translated = GoogleTranslator(source='auto', target='ja').translate(text)
    print("jp: ", translated, "\n")
    return translated

def speech_to_text():
    audio_file= open(file_name, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    print("en: ", transcript.text)
    return transcript.text

def VoiceRecord():
    frames = []
    print("Recording...")
    while keyboard.is_pressed('v'):
        data = stream.read(1024)
        frames.append(data)

    print(f"Recording finished. Saving to {file_name}...")
    sound_file = wave.open(file_name, "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    print(f"Saving complete!")
    asyncio.run(speech(translate(speech_to_text())))

def check_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

if not check_process_running('VOICEVOX.exe'):
    subprocess.Popen(['D:\VoiceVOX\VOICEVOX.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Press and hold 'v' to record.")
while True:
    time.sleep(0.1)
    while keyboard.is_pressed('v'):
        VoiceRecord()