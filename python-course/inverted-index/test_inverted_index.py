from inverted_index_starter import *
def test_can_load_from_file():
    loaded_file = load_documents("test_dataset")
    expected_file = {12: ['anarchismi', 'cat', 'guns', 'test', ''], 13: ['test', 'dog', 'doll', 'house', ''], 14: ['dog', 'test', 'cat', 'doll', '']}
    assert expected_file == loaded_file


def test_can_create_content_list():
    content_list = ""


def test_can_build_inverted_index():
    dataset = load_documents("test_dataset")
    inverted_index = build_inverted_index(dataset)
    #expected_inverted_index = InvertedIndex(documents='{'anarchismi': [12], 'cat': [12, 14], 'guns': [12], 'test': [12, 13, 14], '': [12, 13, 14], 'dog': [13, 14], 'doll': [13, 14], 'house': [13]}')
    #assert expected_inverted_index == inverted_index


def test_can_dump_inverted_index_to_file():
    expected_inverted_index = {'anarchismi': [12], 'cat': [12, 14], 'guns': [12], 'test': [12, 13, 14], '': [12, 13, 14], 'dog': [13, 14], 'doll': [13, 14], 'house': [13]}
    inverted_index = InvertedIndex(expected_inverted_index)
    dump = inverted_index.dump("test_dump")
    #assertEqual(read_status(dump), expected_inverted_index)



def test_can_load_inverted_index_to_runtime():
    pass


def test_can_query_to_inverted_index_and_return_data():
    words = ['cat', 'test']
    documents = {'anarchismi': [12], 'cat': [12, 14], 'guns': [12], 'test': [12, 13, 14], '': [12, 13, 14], 'dog': [13, 14], 'doll': [13, 14], 'house': [13]}
    expected_result = [12, 14]
    result = inverted_index.query(words)
