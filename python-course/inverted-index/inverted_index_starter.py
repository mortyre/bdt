from __future__ import annotations
import re
import json

from typing import Dict, List


class InvertedIndex:
    def __init__(self):
        self.documents: Dict[int, List[int]] = {}

    def __repr__(self):
        _repr = f"{self.__class__.__name__}(documents='{self.documents}')"
        return _repr

    def __eq__(self, rhs):
        pass

    def invert(self, id, words):
        for word in words:
            if word not in self.documents:
                self.documents[word] = [id]
            else:
                self.documents[word].append(id)

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
        return cls(documents)


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
    index = InvertedIndex()

    for id, words in documents.items():
        index.invert(id, words)
    return index


def main():
    documents = load_documents("dataset")
    inverted_index = build_inverted_index(documents)
    inverted_index.dump("dump")
    inverted_index = InvertedIndex.load("dump")
    document_ids = inverted_index.query(["cat", "test"])


if __name__ == "__main__":
    main()
