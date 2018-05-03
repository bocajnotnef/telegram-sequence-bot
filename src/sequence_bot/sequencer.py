#! /usr/bin/env python3

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from typing import Set, Optional
from ._version import get_versions
import argparse
import configparser
import logging
import telegram

__version__: str = get_versions()['version']  # type: ignore
sequence = None
DICTIONARY: Set[str] = set()
WATCHING_CHAT = None
RESPONDING_CHAT = None

CAPITAL_LETTERS = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
CAPITAL_LETTERS_SET = set(CAPITAL_LETTERS)


class BadMessageFormException(Exception):
    pass


class BadMessageSequenceException(Exception):
    pass


class AlphaSequence:
    def __init__(self):
        self.last_letters = None
        self.last_user = None

    def validate(self, message_text, user):

        AlphaSequence._validate_message_form(message_text, user)
        self._validate_message_sequence(message_text, user)

        # import ipdb; ipdb.set_trace()

        if message_text in DICTIONARY:
            return f"Hey {user}, {message_text} is a scrabble word!"

        return None

    @staticmethod
    def _validate_message_form(message_text, user):
        if not all([c in CAPITAL_LETTERS for c in message_text]):
            logging.info(f"Wow, {user} is bad at this.")
            raise BadMessageFormException()

    def _validate_message_sequence(self, message_text, user):
        if self.last_letters is None:
            self.last_letters = AlphaSequence._to_num(message_text)
            self.last_user = user
        else:
            if self.last_letters + 1 == AlphaSequence._to_num(message_text) and self.last_user != user: # NOQA
                self.last_letters = AlphaSequence._to_num(message_text)
                self.last_user = user
                return True
            else:
                self.last_letters = None
                raise BadMessageSequenceException()

    @staticmethod
    def _to_num(stringput):
        val = 0
        for i, ch in enumerate(stringput[::-1]):
            if ch not in CAPITAL_LETTERS_SET:
                return -1
            val += (CAPITAL_LETTERS.index(ch)+1)*(26**(i))
        return val


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def reset(bot, update):
    print("moo")
    global sequence
    sequence.last = None
    logging.info("Reset sequence...")


def validate(bot, update):
    global sequence

    if WATCHING_CHAT is None:
        return

    if update.effective_chat.id != WATCHING_CHAT:
        return

    logging.info(f"I am in chat ID {update.message.chat.id}")
    if update.message:
        logging.info(f"{update.effective_user.username}: {update.message.text}")
        user = update.effective_user.username

        try:
            msg = sequence.validate(update.message.text, user)

            if msg is not None:
                bot.send_message(RESPONDING_CHAT, msg)

        except BadMessageFormException:
            bot.send_message(RESPONDING_CHAT, f"Geez, @{user}, at least try to make it look right.")
        except BadMessageSequenceException:
            bot.send_message(RESPONDING_CHAT, f"@{user} WRONG")

    else:
        logging.info("I don't think that was a message..")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', help="enable debugging mode", action="store_true")
    parser.add_argument('--version', help="output the bot's version and halt.",
                        action='version',
                        version=f"Pepper {__version__}")

    return parser.parse_args()


def main(args: Optional[argparse.Namespace] = None):

    if not args:
        args = get_args()

    global sequence
    global WATCHING_CHAT
    global RESPONDING_CHAT
    global DICTIONARY

    config_profile = "DEFAULT"

    if args.debug:
        config_profile = "DEBUG"

    config = configparser.ConfigParser()
    config.read('config.ini')

    RESPONDING_CHAT = int(config[config_profile]['RESPOND_CHAT'])
    WATCHING_CHAT = int(config[config_profile]['WATCH_CHAT'])
    DICTIONARY_FILENAME = config[config_profile]['DICTIONARY_FILENAME']
    TOKEN = config[config_profile]['TOKEN']

    with open(DICTIONARY_FILENAME, 'r') as dict_file:
        for line in dict_file.readlines():
            DICTIONARY.add(line.strip())

    myself = telegram.Bot(token=TOKEN)
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    print(f"Logged in as {myself.get_me()}")
    sequence = AlphaSequence()

    start_handler = CommandHandler('start', start)
    reset_handler = CommandHandler('reset', reset)
    validate_handler = MessageHandler(Filters.all, validate)

    myself.send_message(RESPONDING_CHAT, "Wow, blacked out there for a second...")

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(reset_handler)
    dispatcher.add_handler(validate_handler)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater.start_polling()


if __name__ == "__main__":
    main(get_args())
