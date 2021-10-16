from __future__ import annotations
import re
import json

from typing import Dict, List


class InvertedIndex:
    def __init__(self, documents: Dict[int, str]):
        self.documents = documents

    def __repr__(self):
        _repr = f"{self.__class__.__name__}(documents='{self.documents}')"
        return _repr

    def __eq__(self, rhs):
        pass

    def query(self, words: List[str]) -> List[int]:
        """Return the list of relevant documents for the given query"""
        a = self.documents[words[0]]
        b = self.documents[words[1]]
        result = set(a).intersection(b)
        result = list(result)
        return result


    def dump(self, filepath: str) -> None:
        with open(filepath, 'w') as f:
            json.dump(self.documents, f)

    @classmethod
    def load(cls, filepath: str) -> InvertedIndex:
        with open(filepath) as f:
            documents = json.load(f)
        return InvertedIndex(documents)


def load_documents(filepath: str) -> Dict[int, str]:
    data = {}
    with open(filepath) as f:
        for line in f:
            doc_id, content = line.lower().split("\t", 1)
            doc_id = int(doc_id)
            words = re.split(r"\W+", content)
            #_data = re.sub('[!@#$,.]', '', _data)
            data[doc_id] = words
    return data



def build_inverted_index(documents: Dict[int, str]) -> InvertedIndex:
    inverted_index = {}
    for document in documents:
        content_list = documents[document]
        for _id in range(len(content_list)):
            if content_list[_id] in inverted_index:
                if document not in inverted_index[content_list[_id]]:
                    inverted_index[content_list[_id]].append(document)
            else:
                inverted_index[content_list[_id]] = [document]
    index = InvertedIndex(inverted_index)
    return index




def main():
    documents = load_documents("dataset")
    inverted_index = build_inverted_index(documents)
    inverted_index.dump("dump")
    inverted_index = InvertedIndex.load("dump")
    document_ids = inverted_index.query(["cat", "test"])


if __name__ == "__main__":
    main()
