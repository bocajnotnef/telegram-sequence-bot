#! /usr/bin/env python3

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import argparse
import configparser
import logging
import telegram

config = configparser.ConfigParser()
config.read('config.ini')

BOT_DEBUG_CHAT_ID = int(config['DEFAULT']['BOT_DEBUG_CHAT_ID'])
LETTERS_META_CHAT = int(config['DEFAULT']['LETTERS_META_CHAT'])
LETTERS_MAIN_CHAT = int(config['DEFAULT']['LETTERS_MAIN_CHAT'])

WATCHING_CHAT = None
RESPONDING_CHAT = None

CAPITAL_LETTERS = [chr(c) for c in range(ord('A'), ord('Z') + 1)]


class AlphaSequence:
    def __init__(self):
        self.last = None

    def validate(self, new_letters):
        if self.last is None:
            self.last = new_letters
            return True
        else:
            if self.get_next(self.last) == new_letters:
                self.last = new_letters
                return True
            else:
                return False

    @staticmethod
    def _list_to_letters(list_of_ords):
        return [chr(l + ord('A')) for l in list_of_ords]

    @staticmethod
    def _letters_to_list(letters):
        return [ord(l) - ord('A') for l in letters]

    @staticmethod
    def _get_next_list(list_of_ords):
        new_list = []
        list_of_ords[-1] += 1
        carry = False
        for index, entry in enumerate(list_of_ords[::-1]):
            if carry:
                new_list.append((entry + 1) % 26)
                carry = False
            else:
                new_list.append((entry + 0) % 26)

            if new_list[-1] == 0 and entry != 0:
                carry = True

        if carry:
            new_list.append(0)

        return new_list[::-1]

    def get_next(self, letters):
        return "".join(str(e) for e in AlphaSequence._list_to_letters(
            AlphaSequence._get_next_list(
                AlphaSequence._letters_to_list(letters)
            )
        ))


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

        if not all([c in CAPITAL_LETTERS for c in update.message.text]):
            logging.info(f"Wow, {update.effective_user.username} is bad at this.")
            bot.send_message(RESPONDING_CHAT, f"Geez, @{update.effective_user.username}, at least try to make it look right.")
        else:
            if sequence.validate(update.message.text):
                pass
            else:
                bot.send_message(RESPONDING_CHAT, f"@{update.effective_user.username} WRONG")

    else:
        logging.info("I don't think that was a message..")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('token', help="Telegram API token")
    parser.add_argument('--debug', help="enable debugging mode", action="store_true")

    return parser.parse_args()


def main(args: argparse.Namespace):
    global sequence
    global WATCHING_CHAT
    global RESPONDING_CHAT

    myself = telegram.Bot(token=args.token)
    updater = Updater(token=args.token)
    dispatcher = updater.dispatcher

    if args.debug:
        WATCHING_CHAT = BOT_DEBUG_CHAT_ID
        RESPONDING_CHAT = BOT_DEBUG_CHAT_ID
    else:
        WATCHING_CHAT = LETTERS_MAIN_CHAT
        RESPONDING_CHAT = LETTERS_META_CHAT

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
