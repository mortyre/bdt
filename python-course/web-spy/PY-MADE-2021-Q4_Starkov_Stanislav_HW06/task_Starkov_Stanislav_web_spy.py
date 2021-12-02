#usr/bin/env python3

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
import logging
import logging.config
import yaml
import requests
from bs4 import BeautifulSoup


URL_GITLAB = "https://about.gitlab.com/features/"


def parse_page(page):
    soup = BeautifulSoup(page, features="html.parser")
    return soup


def callback_gitlab(arguments):
    """Call gitlab parse"""

    response = requests.get(URL_GITLAB)
    page = response.text
    soup = parse_page(page)
    free_products = len(soup.find_all(
        "a",
        attrs={"title": "Available in GitLab SaaS Free"}))
    enterprise_products = len(soup.find_all(
        "a",
        attrs={"title": "Not available in SaaS Free"}))
    products = {
            "free_products": free_products,
            "enterprise_products": enterprise_products
            }
    print("free products: ", products["free_products"])
    print("enterprise products: ", products["enterprise_products"])
    return products


def setup_parser(parser):
    """
    function for setup arguments tool's
    """
    subparsers = parser.add_subparsers(help="choose command")

    build_parser = subparsers.add_parser(
        "gitlab", help="gitlab",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    build_parser.set_defaults(callback=callback_gitlab)



def main():
    """Main function"""
    parser = ArgumentParser(
        description="Web pages parser",
        formatter_class=ArgumentDefaultsHelpFormatter,
        prog="web-spy",
        )
    setup_parser(parser)
    arguments = parser.parse_args()

    arguments.callback(arguments)


if __name__ == "__main__":
    main()
