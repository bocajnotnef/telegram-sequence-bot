from sequence_bot.sequencer import AlphaSequence


class TestAlphaSequence():

    def test_initializing(self):
        alpha = AlphaSequence()

        assert alpha.last_letters is None
        assert alpha.validate('AAA', 'TJ')
        assert alpha.validate('AAB', 'Jake')
        assert not alpha.validate('AAD', 'TJ')

    def test_new_digit(self):
        alpha = AlphaSequence()

        assert alpha.validate('ZZZ', 'TJ')
        assert alpha.validate('AAAA', 'Jake')
        assert alpha.validate('AAAB', 'TJ')

    def test_rollover(self):
        alpha = AlphaSequence()

        assert alpha.validate('AAZ', 'TJ')
        assert alpha.validate('ABA', 'Jake')
        assert alpha.validate('ABB', 'TJ')

    def test_bad_start(self):
        alpha = AlphaSequence()

        assert alpha.validate('A', 'TJ')
        assert alpha.validate('B', 'Jake')
        assert not alpha.validate('3C', 'TJ')

    def test_bad_end(self):
        alpha = AlphaSequence()

        assert alpha.validate('A', 'TJ')
        assert alpha.validate('B', 'Jake')
        assert not alpha.validate('C3', 'TJ')

    def test_repeat_user(self):
        alpha = AlphaSequence()
        assert alpha.validate('A', 'TJ')
        assert alpha.validate('B', 'Jake')
        assert not alpha.validate('C', 'Jake')