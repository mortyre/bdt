#!/usr/bin/env python3
from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys
from typing import List
import re
import json

from typing import Dict, List

DEFAULT_INVERTED_INDEX_PATH = "./dataset"
DEFAULT_INVERTED_INDEX_STORE = "dump"
DEFAULT_INVERTED_INDEX_STRATEGY = "json"


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
        sets: List[set] = []

        for word in words:
            if word in self.documents:
                sets.append(set(self.documents[word]))
            else:
                return list()

        return set.intersection(*sets)

    def dump(self, filepath: str, strategy: str) -> None:
        """Dump documents from Python RunTime to file"""
        if strategy == "json":
            with open(filepath, 'w') as file:
                json.dump(self.documents, file)
        elif strategy == "pickle":
            print("Sorry, this function under developing")
        else:
            print("Sorry. Strategy repl(self.strategy) not supported")

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

def callback_build(arguments):
    """Build inverted index and return it"""
    documents = load_documents(arguments.dataset)
    inverted_index = build_inverted_index(documents)
    inverted_index.dump(arguments.output, arguments.strategy)


def callback_query(arguments):
    inverted_index = InvertedIndex.load(arguments.json_index)
    for words in arguments.query:
        document_ids = inverted_index.query(words)
        print(",".join(str(x) for x in document_ids))
    #return document_ids


def setup_parser(parser):
    """
    function for setup arguments tool's
    """
    subparsers = parser.add_subparsers(help="choose command")

    build_parser = subparsers.add_parser(
        "build", help="build inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    build_parser.add_argument(
        "-d", "--dataset", default=DEFAULT_INVERTED_INDEX_PATH,
        help="set path to dataset, default path is %(default)s",
        )
    build_parser.add_argument(
        "-o", "--output", default=DEFAULT_INVERTED_INDEX_STORE,
        help="path to store dataset, default path is %(default)s",
        )
    build_parser.add_argument(
        "-s", "--strategy", choices=['json', 'pickle'],
        default=DEFAULT_INVERTED_INDEX_STRATEGY,
        help="set strategy to save inverted index, default is %(default)s",
        )
    build_parser.set_defaults(callback=callback_build)

    query_parser = subparsers.add_parser(
        "query", help="build inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    query_parser.add_argument(
        "-i", "--json-index", default=DEFAULT_INVERTED_INDEX_STORE,
        help="path to binary dump",
        )
    query_parser.add_argument(
        "-q", "--query", nargs="+", required=True, metavar="WORD", action='append',
        help="qury to inverted index",
        )
    query_parser.set_defaults(callback=callback_query)

def process_arguments(dataset: str, query: List) -> List:
    pass


def main():
    """Main function"""
    parser = ArgumentParser(
        description="Inverted Index CLI",
        formatter_class=ArgumentDefaultsHelpFormatter,
        prog="inverted-index",
        )
    setup_parser(parser)
    arguments = parser.parse_args()

    arguments.callback(arguments)


if __name__ == "__main__":
    main()
