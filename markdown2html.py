#!/usr/bin/python3
"""Markdonw module"""
import sys

def main():
    """
    The main function of the script.
    It checks the command line arguments and processes the Markdown file.
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    try:
        with open(markdown_file, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()