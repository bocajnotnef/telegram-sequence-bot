# What is this?

This is a bot that monitors chats in which users sequentially 'increment' messages like 'AAAAA', and 'AAAAB' for fun.
It will inform people if they're wrong.

## Why?

We also have a counting chat that's bot enforced. This chat spun up as a joke, but I wanted to learn the Python bot framework. Seemed fun.

## You need a life

Yeah, probably.

# Overview

We use the [Python Telegram Bot Framework](https://github.com/python-telegram-bot/python-telegram-bot) for API access.

The validation of the sequence itself takes place in the `AlphaSequence` class.

The validation of the message format takes place in the `validate()` method.

Config filename is `config.ini` and the format should be:

```
[DEFAULT]
RESPOND_CHAT = 99999999
WATCH_CHAT = 99999999
TOKEN = KEYKEYKEYKEYKEYKEYKEYKEYKEYKEY
DICTIONARY_FILENAME = dictionary.txt

[DEBUG]
WATCH_CHAT = 99999999
RESPOND_CHAT = 99999999
TOKEN = KEYKEYKEYKEYKEYKEYKEYKEYKEYKEY
DICTIONARY_FILENAME = dictionary.txt

```

Eventually, we'll store things like insults in there, too

## Dictionary

Dictionary pulled in from https://raw.githubusercontent.com/jonbcard/scrabble-bot/master/src/dictionary.txt