#!/usr/bin/python3
"""Markdown to HTML converter module"""
import sys

def parse_heading(line):
    """
    Converts a Markdown heading to an HTML heading.
    """
    if line.startswith("#"):
        level = line.count('#')  
        line_content = line.strip('#').strip()
        return f"<h{level}>{line_content}</h{level}>"
    return line

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
            with open(html_file, 'w') as html:
                for line in f:
                    html_line = parse_heading(line)
                    html.write(html_line + '\n')
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
