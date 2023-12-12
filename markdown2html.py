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

def parse_list(line, in_list, list_type):
    """
    Converts a Markdown list item to an HTML list item.
    Handles both ordered and unordered lists.
    Returns the HTML line and a flag indicating if we are currently inside a list.
    """
    if line.startswith(("- ", "* ")):
        if not in_list:
            tag = "ul" if line.startswith("- ") else "ol"
            return f"<{tag}>\n<li>" + line[2:].strip() + "</li>", True, tag
        else:
            return "<li>" + line[2:].strip() + "</li>", True, list_type
    else:
        if in_list:
            return f"</{list_type}>\n" + line, False, None
        else:
            return line, in_list, list_type

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
                in_list = False
                list_type = None
                for line in f:
                    html_line, in_list, list_type = parse_list(parse_heading(line), in_list, list_type)
                    html.write(html_line + '\n')
                if in_list:
                    html.write(f"</{list_type}>\n")
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
