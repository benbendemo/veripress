from pytest import raises

from veripress.helpers import *


def test_to_list():
    assert to_list(123) == [123]
    assert to_list([1, 2, 3]) == [1, 2, 3]
    assert to_list(('a', 'b', 'c')) == ['a', 'b', 'c']
    assert to_list('abc') == ['abc']
    assert to_list(b'abc') == [b'abc']
    assert to_list(filter(lambda x: x > 2, [1, 2, 3, 4])) == [3, 4]


def test_to_datetime():
    d = date(year=2016, month=10, day=22)
    dt = datetime.strptime('2016/10/22', '%Y/%m/%d')
    assert isinstance(to_datetime(d), datetime)
    assert to_datetime(d) == dt
    assert id(to_datetime(dt)) == id(dt)
    assert to_datetime('other things') == 'other things'


def test_configuration_error():
    with raises(Exception, message='Storage type "database" if not supported'):
        raise ConfigurationError('Storage type "database" if not supported')


def test_url_rule():
    class FakeBlueprint(object):
        def __init__(self):
            self.rules = []

        def add_url_rule(self, rule, **kwargs):
            self.rules.append(rule)

    fake_bp = FakeBlueprint()
    url_rule(fake_bp, '/posts/')
    url_rule(fake_bp, ['/posts/<int:post_id>'])
    assert fake_bp.rules == ['/posts/', '/posts/<int:post_id>']


def test_pair():
    pair = Pair()
    assert pair.first is None and pair.second is None
    assert not pair

    pair = Pair(1, 'a')
    assert pair
    assert pair == Pair(1, 'a')
    assert pair != []
    assert 1 in pair and 'a' in pair
    assert 2 not in pair
    a, b = pair
    assert a == 1 and b == 'a'
    assert '(1, \'a\')' in repr(pair)

    pair += (2, 'b')
    assert pair == Pair(3, 'ab')
    with raises(ValueError):
        pair += (1, 2, 3)
    with raises(TypeError):
        pair += ('a', 2)

    assert Pair(100, 200) - Pair(100, 200) == Pair(0, 0)

    pair = Pair(2, 'b')
    assert pair[0] == 2
    assert pair[1] == 'b'
    with raises(IndexError):
        a = pair[2]
