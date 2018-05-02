from sequence_bot.sequencer import AlphaSequence, BadMessageFormException, BadMessageSequenceException # NOQA
from sequence_bot import sequencer
import pytest
from unittest.mock import MagicMock
from bunch import Bunch


class TestValidationHandler():
    def setup_method(self, method):
        sequencer.WATCHING_CHAT = None
        sequencer.sequence = None
        sequencer.DICTIONARY = set()
        sequencer.RESPONDING_CHAT = None

    def test_validate_no_watching_chat(self):
        sequencer.WATCHING_CHAT = None
        bot = Bunch()
        update = Bunch()

        assert sequencer.validate(bot, update) is None

    def test_validate_wrong_watching_chat(self):
        sequencer.WATCHING_CHAT = "SomethingElse"
        bot = Bunch()
        update = Bunch(effective_chat=Bunch(id="NotThat"))

        assert sequencer.validate(bot, update) is None

    def test_validate_no_message(self):
        sequencer.WATCHING_CHAT = "ThatThing"
        sequencer.sequence = AlphaSequence()

        bot = object()

        update = Bunch(
            effective_chat=Bunch(
                id="ThatThing"
            ),
            effective_user=Bunch(
                username="Jake"
            ),
            message=Bunch(
                text="AA",
                chat=Bunch(
                    id="ThatThing"
                ),
            )
        )

        assert sequencer.validate(bot, update) is None

    def test_validate_scrabble_message(self):
        sequencer.WATCHING_CHAT = "ThatThing"
        sequencer.sequence = AlphaSequence()
        sequencer.DICTIONARY.add('AARDVARK')
        sequencer.RESPONDING_CHAT = "RESPONSE_CHAT"

        bot = Bunch(send_message=MagicMock(name="send_message"))

        update = Bunch(
            effective_chat=Bunch(
                id="ThatThing"
            ),
            effective_user=Bunch(
                username="Jake"
            ),
            message=Bunch(
                text="AARDVARK",
                chat=Bunch(
                    id="ThatThing"
                ),
            )
        )

        assert sequencer.validate(bot, update) is None

        bot.send_message.assert_called_once_with(
            "RESPONSE_CHAT",
            "Hey Jake, AARDVARK is a scrabble word!"
        )

    def test_validate_bad_message_form(self):
        sequencer.WATCHING_CHAT = "ThatThing"
        sequencer.sequence = AlphaSequence()
        sequencer.DICTIONARY.add('AARDVARK')
        sequencer.RESPONDING_CHAT = "RESPONSE_CHAT"

        bot = Bunch(send_message=MagicMock(name="send_message"))

        update = Bunch(
            effective_chat=Bunch(
                id="ThatThing"
            ),
            effective_user=Bunch(
                username="Jake"
            ),
            message=Bunch(
                text="oh no I broke letters again",
                chat=Bunch(
                    id="ThatThing"
                ),
            )
        )

        assert sequencer.validate(bot, update) is None

        bot.send_message.assert_called_once_with(
            "RESPONSE_CHAT",
            "Geez, @Jake, at least try to make it look right."
        )

    def test_validate_bad_message_sequence(self):
        sequencer.WATCHING_CHAT = "ThatThing"
        sequencer.sequence = AlphaSequence()
        sequencer.DICTIONARY.add('AARDVARK')
        sequencer.RESPONDING_CHAT = "RESPONSE_CHAT"

        bot = Bunch(send_message=MagicMock(name="send_message"))

        update = Bunch(
            effective_chat=Bunch(
                id="ThatThing"
            ),
            effective_user=Bunch(
                username="Jake"
            ),
            message=Bunch(
                text="AA",
                chat=Bunch(
                    id="ThatThing"
                ),
            )
        )

        assert sequencer.validate(bot, update) is None

        update = Bunch(
            effective_chat=Bunch(
                id="ThatThing"
            ),
            effective_user=Bunch(
                username="Jake"
            ),
            message=Bunch(
                text="AC",
                chat=Bunch(
                    id="ThatThing"
                ),
            )
        )

        assert sequencer.validate(bot, update) is None

        bot.send_message.assert_called_once_with(
            "RESPONSE_CHAT",
            "@Jake WRONG"
        )


class TestAlphaSequence():

    def test_initializing(self):
        alpha = AlphaSequence()

        assert alpha.last_letters is None
        assert alpha.validate('AAA', 'TJ') is None
        assert alpha.validate('AAB', 'Jake') is None

        with pytest.raises(BadMessageSequenceException):
            assert alpha.validate('AAD', 'TJ')

    def test_new_digit(self):
        alpha = AlphaSequence()

        assert alpha.validate('ZZZ', 'TJ') is None
        assert alpha.validate('AAAA', 'Jake') is None
        assert alpha.validate('AAAB', 'TJ') is None

    def test_rollover(self):
        alpha = AlphaSequence()

        assert alpha.validate('AAZ', 'TJ') is None
        assert alpha.validate('ABA', 'Jake') is None
        assert alpha.validate('ABB', 'TJ') is None

    def test_bad_start(self):
        alpha = AlphaSequence()

        assert alpha.validate('A', 'TJ') is None
        assert alpha.validate('B', 'Jake') is None

        with pytest.raises(BadMessageFormException):
            alpha.validate('3C', 'TJ')

    def test_bad_end(self):
        alpha = AlphaSequence()

        assert alpha.validate('A', 'TJ') is None
        assert alpha.validate('B', 'Jake') is None

        with pytest.raises(BadMessageFormException):
            alpha.validate('C3', 'TJ')

    def test_repeat_user(self):
        alpha = AlphaSequence()
        assert alpha.validate('A', 'TJ') is None
        assert alpha.validate('B', 'Jake') is None

        with pytest.raises(BadMessageSequenceException):
            alpha.validate('C', 'Jake')

    def test_scrabble_word(self):
        alpha = AlphaSequence()

        # dictionary doesn't initialize if we don't run main
        sequencer.DICTIONARY.add('AARDVARK')

        assert alpha.validate('AARDVARK', 'Jake') == "Hey Jake, AARDVARK is a scrabble word!" # NOQA
