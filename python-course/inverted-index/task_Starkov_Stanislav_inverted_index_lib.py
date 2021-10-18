from __future__ import annotations
import re
import json

from typing import Dict, List


class InvertedIndex:
    """Main Class for work with index"""
    def __init__(self, docs: Dict[int, List[int]] = {}):
        """Constructer"""
        self.documents: Dict[int, List[int]] = docs

    def __repr__(self):
        _repr = f"{self.__class__.__name__}(documents='{self.documents}')"
        return _repr

    def __eq__(self, documents):
        return True

    def invert(self, doc_id, words):
        """Invert dict"""
        for word in words:
            if word not in self.documents:
                self.documents[word] = [doc_id]
            else:
                self.documents[word].append(doc_id)

    def query(self, words: List[str]) -> List[int]:
        """Return the list of relevant documents for the given query"""
        result: set = set()

        for word in words:
            if word in self.documents:
                result = result.intersection(self.documents[word])
                #result = result.union(self.documents[word])

        return list(result)
#        try:
#            first_word = self.documents[words[0]]
#            second_word = self.documents[words[1]]
#            result = set(first_word).intersection(second_word)
#            result = list(result)
#            return result
#        except Exception:
#            print("Some word is not found")

    def dump(self, filepath: str) -> None:
        """Dump documents from Python RunTime to file"""
        with open(filepath, 'w') as file:
            json.dump(self.documents, file)

    @classmethod
    def load(cls, filepath: str) -> InvertedIndex:
        """Load inverted dump from file to Python RunTime"""
        with open(filepath) as file:
            documents = json.load(file)
        return cls(documents)


def load_documents(filepath: str) -> Dict[int, str]:
    """Load source dumcuments from file to runtime.
    Supported format: ID <TAB> Text"""
    data = {}
    with open(filepath, encoding="utf-8") as file:
        for line in file:
            doc_id, content = line.strip().lower().split("\t", 1)
            doc_id = int(doc_id)
            data[doc_id] = content
    return data


def build_inverted_index(documents: Dict[int, str]) -> InvertedIndex:
    """Build inverted index in object"""
    index = InvertedIndex()

    for doc_id, words in documents.items():
        words = re.split(r"\W+", words)
        index.invert(doc_id, words)
    return index


def main():
    """Main function"""
    documents = load_documents("dataset")
    inverted_index = build_inverted_index(documents)
    inverted_index.dump("dump")
    inverted_index = InvertedIndex.load("dump")
    document_ids = inverted_index.query(["the", "is"])
    return document_ids


if __name__ == "__main__":
    main()
