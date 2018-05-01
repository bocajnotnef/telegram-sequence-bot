from sequence_bot.sequencer import AlphaSequence


class TestAlphaSequence():

    def test_initializing(self):
        alpha = AlphaSequence()

        assert(alpha.last is None)
        assert(alpha.validate('AAA'))
        assert(alpha.validate('AAB'))
        assert not alpha.validate('AAD')
