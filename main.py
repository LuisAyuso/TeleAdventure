#!/usr/bin/python
"""
test test test
"""

from telegram import (Updater, ChatAction)
import ConfigParser
import os
import logging

from subprocess import Popen, PIPE


# Enable logging
formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=formatstr, level=logging.INFO)

logger = logging.getLogger(__name__)

active_games = dict()


class Game:

    game_stream = None

    def __init__(self):
        print "new game"
        self.game_stream = Popen(['frotz', '/home/luis/code/tele-adventure/games/zork_1.z5'], stdout=PIPE, stderr=PIPE)

    def read_game_status(self):

        text = ""
        byte = self.game_stream.stdout.read(1)
        while byte != "":
            text = text + byte
            byte = self.game_stream.stdout.read(1)
        return text


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi, lets play something!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help! i need somebody:')
    bot.sendMessage(update.message.chat_id, text='/list_games: what games are installed')
    bot.sendMessage(update.message.chat_id, text='/start_game: start a new game')


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
        echo(bot, update)

    return process_message


def ls_closure(config):

    def ls_command_handle(bot, update):

        games = config["games"]
        for f in os.listdir(games):
            bot.sendMessage(update.message.chat_id, f)

    return ls_command_handle


def start_closure(config):

    def start_command_handle(bot, update):

        # make sure user is not playing
        user = update.message.from_user
        if user.id not in active_games:
            active_games[user.id] = Game()
        else:
            bot.sendMessage(update.message.chat_id, "already in game")

        text = active_games[user.id].read_game_status()
        bot.sendMessage(update.message.chat_id, text)

    return start_command_handle


def main():

    cnf = loadConfig()
    TOKEN = cnf["token"]
    games = cnf["games"]
    print "donwloads in: ", games

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("list_games", ls_closure(cnf))
    dp.addTelegramCommandHandler("start_game", start_closure(cnf))

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
