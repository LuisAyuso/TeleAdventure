#!/usr/bin/python
"""
test test test
"""

from telegram import (Updater, ChatAction)
import ConfigParser
import os
from text_game import Game

active_games = dict()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi, lets play something!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help! i need somebody:')
    bot.sendMessage(update.message.chat_id, text='/list_games: what games are installed')
    bot.sendMessage(update.message.chat_id, text='/start_game: start a new game')


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

        if len(update.message.text) != 0:

            user = update.message.from_user
            if user.id not in active_games:
                bot.sendMessage(update.message.chat_id, "not in game")
            else:
                command = update.message.text
                print " send input: ", command
                active_games[user.id].send_input(command)
                print " read output: "
                text = active_games[user.id].read_game_status()
                print " send back "
                if len(text) > 0:
                    # remove echo from sent message
                    bot.sendMessage(update.message.chat_id, text=text)

    return process_message


def ls_closure(config):

    def ls_command_handle(bot, update):

        games = config["games"]
        for f in os.listdir(games):
            bot.sendMessage(update.message.chat_id, f)

    return ls_command_handle


def start_closure(config):

    def start_command_handle(bot, update):
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)

        # make sure user is not playing
        user = update.message.from_user
        if user.id not in active_games:
            print "start game"
            active_games[user.id] = Game()
            print "game started"
        else:
            bot.sendMessage(update.message.chat_id, "already in game")
        bot.sendMessage(update.message.chat_id, "lets play!")
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)

        text = active_games[user.id].read_game_status()
        if len(text) > 0:
                bot.sendMessage(update.message.chat_id, text)

    return start_command_handle


def update_cmd(bot, update):

        user = update.message.from_user
        text = active_games[user.id].read_game_status()
        if len(text) > 0:
                bot.sendMessage(update.message.chat_id, text)


def main():

    cnf = loadConfig()
    TOKEN = cnf["token"]
    games = cnf["games"]
    print "games in: ", games

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("list_games", ls_closure(cnf))
    dp.addTelegramCommandHandler("start_game", start_closure(cnf))
    dp.addTelegramCommandHandler("update", update_cmd)

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
