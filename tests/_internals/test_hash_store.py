# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# type: ignore

from os import unlink
from tempfile import NamedTemporaryFile
from unittest.mock import patch

from src._internals.hash_store import calculate_file_hash, filter_indexed_files, list_indexed_hashes, store_hash


def test_filter_indexed_files():

    # arrange
    source_files = {'file1.pdf': '2473772b5e9519befc4c87f80599d614', 'file4.pdf': 'b6fec6100be93b50d7ea0f115e15267a'}
    indexed_hashes = ['2473772b5e9519befc4c87f80599d614']
    expected = {'file4.pdf': 'b6fec6100be93b50d7ea0f115e15267a'}

    with patch('src._internals.hash_store.list_indexed_hashes', return_value=indexed_hashes), \
         patch('src._internals.hash_store.calculate_file_hash', side_effect=lambda filepath: source_files[filepath]):

        # act
        actual = filter_indexed_files('my_file.txt', source_files.keys())

        # assert
        assert actual == expected


def test_list_indexed_hashes_none():

    # arrange
    expected = set()

    # act
    actual = list_indexed_hashes('my_file.txt')

    # asssert
    assert actual == expected


def test_list_indexed_hashes_multiple():

    temporary_filepath = _create_temporary_file(
        b'f923637121bf9141025283ecbfaecfb4\n4d2f305e66615ed3349d02417a1541f4\n')

    try:

        # arrange
        expected = {'f923637121bf9141025283ecbfaecfb4', '4d2f305e66615ed3349d02417a1541f4'}

        # act
        actual = list_indexed_hashes(temporary_filepath)

        # assert
        assert actual == expected

    finally:
        unlink(temporary_filepath)


def test_store_hash():

    temporary_filepath = _create_temporary_file()

    try:

        # arrange
        filehash = '85a3d71a6c0d7da43946ed643f5d7d4b'
        expected = f'{filehash}\n'

        # act
        store_hash(temporary_filepath, filehash)

        # assert
        with open(temporary_filepath, 'r', encoding='utf-8') as f:
            actual = f.read()
        assert actual == expected

    finally:
        unlink(temporary_filepath)


def test_calculate_file_hash():

    temporary_filepath = _create_temporary_file(b'hello world')

    try:

        # arrange
        expected = '5eb63bbbe01eeed093cb22bb8f5acdc3'

        # act
        actual = calculate_file_hash(temporary_filepath)

        # assert
        assert actual == expected

    finally:
        unlink(temporary_filepath)


def _create_temporary_file(content: str = None) -> str:

    with NamedTemporaryFile(delete=False) as temporary_file:
        if content:
            temporary_file.write(content)

    return temporary_file.name
