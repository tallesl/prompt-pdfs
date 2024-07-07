# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# type: ignore

from src._internals.utilities import get_printable_list


def test_get_printable_list_empty():

    # arrange
    items = []
    expected = ' (none)'

    # act
    actual = get_printable_list(items)

    # assert
    assert actual == expected


def test_get_printable_list_single():

    # arrange
    items = ['foo']
    expected = '\n\tfoo'

    # act
    actual = get_printable_list(items)

    # assert
    assert actual == expected


def test_get_printable_list_multiple():

    # arrange
    items = ['foo', 'bar', 'qux']
    expected = '\n\tbar\n\tfoo\n\tqux'

    # act
    actual = get_printable_list(items)

    # assert
    assert actual == expected
