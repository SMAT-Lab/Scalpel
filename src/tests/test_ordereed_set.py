import sys
from unittest import TestCase
from scalpel._duc import ordered_set as ordered_set
if sys.version_info.major >= 3:
    class OrderedSetTest(TestCase):

        def test_add(self):
            x = ordered_set([1, 2, -1, "bar"])
            x.add(0)
            assert list(x) == [1, 2, -1, "bar", 0]


        def test_discard(self):
            x = ordered_set([1, 2, -1])
            x.discard(2)
            assert list(x) == [1, -1]


        def test_discard_ignores_missing_element(self):
            x = ordered_set()
            x.discard(1)  # This does not raise


        def test_remove(self):
            x = ordered_set([1])
            x.remove(1)
            assert not x


        def test_remove_raises_missing_element(self):
            x = ordered_set()
            try:
                x.remove(1)
            except KeyError:
                pass
            else:
                raise AssertionError('Should have raised IndexError')


        def test_getitem(self):
            x = ordered_set([1, 2, -1])
            assert x[0] == 1
            assert x[1] == 2
            assert x[2] == -1
            try:
                x[3]
            except IndexError:
                pass
            else:
                raise AssertionError('Should have raised IndexError')


        def test_len(self):
            x = ordered_set([1])
            assert len(x) == 1


        def test_iter(self):
            for x in ordered_set([1]):
                assert x == 1


        def test_str(self):
            x = ordered_set([1, 2, 3])
            assert str(x) == "{1, 2, 3}"


        def test_repr(self):
            x = ordered_set([1, 2, 3])
            assert repr(x) == "<ordered_set {1, 2, 3}>"


        def test_eq(self):
            x = ordered_set([1, 2, 3])
            y = ordered_set([1, 2, 3])
            assert x == y
            assert x is not y


        def test_init_empty(self):
            x = ordered_set()
            assert len(x) == 0
            x.add(2)
            assert len(x) == 1

        def test_dunder_add(self):
            x = ordered_set([1, 2, 3])
            y = ordered_set([1, 2, 3])
            z = ordered_set([2, 4])
            assert x+y == x
            assert x+z == ordered_set([1, 2, 3, 4])

        def test_update(self):
            x = ordered_set([1, 2, 3])
            x.update([1, 2, 3])
            assert x == ordered_set([1, 2, 3])
            x.update(ordered_set([1, 2, 3, 4]))
            assert x == ordered_set([1, 2, 3, 4])
