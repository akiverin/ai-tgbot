# coding: utf-8
from telegram import Update
from telegram.ext import CallbackContext
from dialogues import bot, stats
import speech_recognition as sr
from gtts import gTTS
import os


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def run_bot(update: Update, context: CallbackContext) -> None:
    replica = update.message.text
    answer = bot(replica)
    update.message.reply_text(answer)

    print(stats)
    print(replica)
    print(answer)
    print()


def handle_voice(update: Update, context: CallbackContext) -> None:
    voice_file = context.bot.get_file(update.message.voice.file_id)
    file_path = "voice.ogg"
    wav_path = "voice.wav"
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)
    voice_file.download(file_path)
    os.system('ffmpeg -i voice.ogg voice.wav')

    recognizer = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Recognized text: {text}")
            answer = bot(text)

            tts = gTTS(text=answer, lang='ru')
            tts.save('answer.mp3')
            context.bot.send_voice(chat_id=update.effective_chat.id, voice=open('answer.mp3', 'rb'))

        except sr.UnknownValueError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось распознать речь.")
        except sr.RequestError as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка сервиса распознавания речи.")
