# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# type: ignore

from datetime import datetime
from io import StringIO
from unittest.mock import patch
import sys

from src._internals.utilities import get_printable_list, log


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


def test_log():

    # arrange
    with patch('src._internals.utilities.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 2, 3, 4, 5)

        with StringIO() as captured_output:
            original_stdout = sys.stdout
            sys.stdout = captured_output

            expected_output = '[03:04:05] Test message\n'

            try:
                # act
                log('Test message')
                actual = captured_output.getvalue()

                # assert
                assert actual == expected_output

            finally:
                sys.stdout = original_stdout
