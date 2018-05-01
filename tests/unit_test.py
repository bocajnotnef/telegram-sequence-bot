from sequence_bot.sequencer import AlphaSequence


class TestAlphaSequence():

    def test_initializing(self):
        alpha = AlphaSequence()

        assert(alpha.last is None)
        assert(alpha.validate('AAA'))
        assert(alpha.validate('AAB'))
        assert not alpha.validate('AAD')

    def test_new_digit(self):
        alpha = AlphaSequence()

        assert(alpha.validate('ZZZ'))
        assert(alpha.validate('AAAA'))
        assert(alpha.validate('AAAB'))

    def test_rollover(self):
        alpha = AlphaSequence()

        assert(alpha.validate('AAZ'))
        assert(alpha.validate('ABA'))
        assert(alpha.validate('ABB'))

    def test_bad_start(self):
        alpha = AlphaSequence()

        assert(alpha.validate('A'))
        assert(alpha.validate('B'))
        assert not alpha.validate('3C')

    def test_bad_end(self):
        alpha = AlphaSequence()

        assert(alpha.validate('A'))
        assert(alpha.validate('B'))
        assert not alpha.validate('C3')
