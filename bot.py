# coding: utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import start, help_command, run_bot, handle_voice


def main():
    updater = Updater("6845729797:AAG7EKhiXQfBddCrizOfdtmtj9rcS3Zbb6A")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, run_bot))
    dispatcher.add_handler(MessageHandler(Filters.voice, handle_voice))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


