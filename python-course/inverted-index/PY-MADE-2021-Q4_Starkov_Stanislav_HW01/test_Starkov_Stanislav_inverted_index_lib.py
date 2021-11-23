from task_Starkov_Stanislav_inverted_index_lib import *

def test_can_load_from_file():
    loaded_file = load_documents("test_dataset")
    expected_file = {12: 'anarchismi cat, guns test',
                     13: 'test dog doll house.',
                     14: 'dog test cat doll!'}
    assert expected_file == loaded_file


def test_can_build_inverted_index():
    dataset = load_documents("test_dataset")
    inverted_index = build_inverted_index(dataset)
    documents = {'anarchismi': [12], 'cat': [12, 14], 'guns': [12], 'test': [12, 13, 14],
                 '': [12, 13, 14], 'dog': [13, 14], 'doll': [13, 14], 'house': [13]}
    expected_inverted_index = InvertedIndex(documents)
    assert expected_inverted_index == inverted_index


def test_can_dump_inverted_index_to_file():
    documents = {'anarchismi': [12], 'cat': [12, 14], 'guns': [12], 'test': [12, 13, 14],
                 '': [12, 13, 14], 'dog': [13, 14], 'doll': [13, 14], 'house': [13]}
    expected_inverted_index = InvertedIndex(documents)
    expected_inverted_index.dump("test_dump")
    test_dump = open("test_dump", "r")
    assert expected_inverted_index == test_dump.read()



def test_can_load_inverted_index_to_runtime():
    inverted_index = InvertedIndex()
    inverted_index = inverted_index.load("test_dump")
    test_dump = open("test_dump", "r")
    assert inverted_index == test_dump.read()



def test_can_query_to_inverted_index_and_return_data():
    words = ['cat', 'test']
    documents = {'anarchismi': [12], 'cat': [12, 14], 'guns': [12], 'test': [12, 13, 14],
                 '': [12, 13, 14], 'dog': [13, 14], 'doll': [13, 14], 'house': [13]}
    expected_result = [12, 14]
    inverted_index = InvertedIndex(documents)
    assert expected_result == inverted_index.query(words)
