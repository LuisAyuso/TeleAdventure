#!/usr/bin/python
"""
test test test
"""

from telegram import (Updater, ChatAction, Document)
import ConfigParser
import os
import logging


# Enable logging
formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=formatstr, level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hola hola!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help! i need somebody')


def echo(bot, update):

    if len(update.message.text) == 0:
        bot.sendMessage(update.message.chat_id, "message not undestood")
    else:
        bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def loadConfig():

    config = ConfigParser.ConfigParser()
    config.readfp(open('etc/server.cfg'))

    cnf = {}
    for k, v in config.items("master"):
        cnf[k] = v

    return cnf


def process_message_closure(config):

    def process_message(bot, update):

        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)

        downloads = config["downloads"]

        if len(update.message.text) != 0:
            print "message with text", update.message.text
        if update.message.photo is not None:
            print "message with photo"
        if update.message.video is not None:
            print "message with video"
        if update.message.document is not None:
            print "message with docu", update.message.document
            f = bot.getFile(update.message.document.file_id)
            print "file: ", f
            f.download(downloads + "/" + update.message.document.file_name)
        echo(bot, update)

    return process_message


def ls_closure(config):

    def ls_command_handle(bot, update):

        downloads = config["downloads"]
        for f in os.listdir(downloads):
            bot.sendMessage(update.message.chat_id, f)

    return ls_command_handle


def get_closure(config):

    def get_command_handle(bot, update):

        downloads = config["downloads"]

        filename = update.message.text[4:]
        filename = downloads + "/" + filename.lstrip()

        if os.path.exists(filename):
            bot.sendMessage(update.message.chat_id, "file exists! " + filename)
         "   f = open(filename, 'r')
         "   dump = f.read()

         "   Document.de_json(dump)

         "   bot.sendDocument

        else:
            bot.sendMessage(update.message.chat_id, "file not found " + filename)

    return get_command_handle


def main():

    cnf = loadConfig()
    TOKEN = cnf["token"]
    downloads = cnf["downloads"]
    print "donwloads in: ", downloads

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("ls", ls_closure(cnf))
    dp.addTelegramCommandHandler("get", get_closure(cnf))

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(process_message_closure(cnf))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
