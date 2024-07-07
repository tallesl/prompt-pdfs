# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# type: ignore

from datetime import datetime
from io import StringIO
from signal import SIGINT, SIGTERM
from unittest.mock import patch, ANY
import sys

from src._internals.utilities import get_printable_list, log, set_signals


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


@patch('src._internals.utilities.datetime')
@patch('sys.stdout', new_callable=StringIO)
def test_log(mock_stdout, mock_datetime):

    # arrange
    mock_datetime.now.return_value = datetime(2024, 1, 2, 3, 4, 5)
    expected = '[03:04:05] Test message\n'

    # act
    log('Test message')
    actual = mock_stdout.getvalue()

    # assert
    assert actual == expected


@patch('src._internals.utilities.signal')
def test_set_signals(mock_signal):
    # act
    set_signals()

    # assert
    assert mock_signal.call_count == 2
    mock_signal.assert_any_call(SIGINT, ANY)
    mock_signal.assert_any_call(SIGTERM, ANY)
