#!/usr/bin/env python3
from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
from io import TextIOWrapper
import sys
from typing import List
import re
import json
import logging
import logging.config
import yaml

from typing import Dict, List

logger = logging.getLogger(__name__)

DEFAULT_INVERTED_INDEX_PATH = "./dataset"
DEFAULT_INVERTED_INDEX_STORE = "dump"
DEFAULT_INVERTED_INDEX_STRATEGY = "struct"

class EncodedFileType(FileType):
    def __call__(self, string):
        # the special argument "-" means sys.std{in,out}
        if string == '-':
            if 'r' in self._mode:
                stdin = TextIOWrapper(sys.stdin.buffer, encoding=self._encoding)
                return stdin
            elif 'w' in self._mode:
                stdout = TextIOWrapper(sys.stdout.buffer, encoding=self._encoding)
                return stdout
            else:
                msg = _('argument "-" with mode %r') % self._mode
                raise ValueError(msg)

        # all other arguments are used as file names
        try:
            return open(string, self._mode, self._bufsize, self._encoding,
                        self._errors)
        except OSError as e:
            args = {'filename': string, 'error': e}
            message = _("can't open '%(filename)s': %(error)s")
            raise ArgumentTypeError(message % args)


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
        elif strategy == "struct":
            logger.info("Sorry, this function under developing")
        else:
            logger.info("Sorry. Strategy %snot supported", repl(self.strategy))

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
    """comments"""
    inverted_index = InvertedIndex.load(arguments.index)
    query = []
    if not arguments.query:
        for line in arguments.query_file:
            line = line.strip().split()
            query.append(line)
    else:
        query = arguments.query

    for words in query:
        document_ids = inverted_index.query(words)
        print(",".join(str(x) for x in document_ids))


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
        "-s", "--strategy", choices=['json', 'struct'],
        default=DEFAULT_INVERTED_INDEX_STRATEGY,
        help="set strategy to save inverted index, default is %(default)s",
        )
    build_parser.set_defaults(callback=callback_build)

    query_parser = subparsers.add_parser(
        "query", help="build inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    query_parser.add_argument(
        "-i", "--index", default=DEFAULT_INVERTED_INDEX_STORE,
        help="path to binary dump",
        )
    query_parser_group = query_parser.add_mutually_exclusive_group(required=True)
    query_parser_group.add_argument(
        "-q", "--query", nargs="+", metavar="WORD", action='append',
        help="qury to inverted index",
        )
    query_parser_group.add_argument(
        "--query-file-utf8",
        dest="query_file", type=EncodedFileType("r", encoding="utf-8"),
        default=TextIOWrapper(sys.stdin.buffer, encoding="utf-8"),
        help="query to inverted index from file UTF-8",
        )
    query_parser_group.add_argument(
        "--query-file-cp1251",
        dest="query_file", type=EncodedFileType("r", encoding="cp1251"),
        default=TextIOWrapper(sys.stdin.buffer, encoding="cp1251"),
        help="query to inverted index from file CP-1251",
        )
    query_parser.set_defaults(callback=callback_query)

def process_arguments(dataset: str, query: List) -> List:
    pass


def setup_logger():
#    logging.basicConfig(
#        filename="inverted_index.log",
#        format="%(asctime)s %(levelname)s %(message)s",
#        datefmt="%Y-%m-%d %H:%M:%S",
#        level=logging.DEBUG
#            )
    with open("logging.conf.yaml") as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin))

def main():
    """Main function"""
    setup_logger()
    parser = ArgumentParser(
        description="Inverted Index CLI",
        formatter_class=ArgumentDefaultsHelpFormatter,
        prog="inverted-index",
        )
    setup_parser(parser)
    arguments = parser.parse_args()
    logger.debug(arguments)

    arguments.callback(arguments)


if __name__ == "__main__":
    main()
