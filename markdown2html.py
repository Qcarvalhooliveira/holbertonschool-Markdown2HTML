#!/usr/bin/python3
"""Markdown to HTML converter module"""
import sys
import re
import hashlib


def convert_md5(text):
    """
    Converts a given text to its MD5 hash.
    """
    return hashlib.md5(text.encode()).hexdigest()

def parse_special_syntax(line):
    """
    Converts special Markdown syntax to HTML or other formats.
    """
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: convert_md5(m.group(1)), line)

    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)

    return line

def parse_bold_and_emphasis(line):
    """
    Converts Markdown bold and emphasis syntax to HTML tags.
    """
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
    return line

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

def parse_paragraphs(lines):
    """
    Converts blocks of text to HTML paragraphs.
    """
    in_paragraph = False
    html_lines = []
    for line in lines:
        if line.startswith(("<h", "</ul>", "</ol>")):
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            html_lines.append(line)
        elif line.startswith(("<ul", "<li", "<ol")):
            if in_paragraph:
                in_paragraph = False
            html_lines.append(line)
        elif line.strip() == "":
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
        else:
            if not in_paragraph and line != "":
                html_lines.append("<p>")
                in_paragraph = True
            elif in_paragraph:
                html_lines.append("<br />")
            html_lines.append(line)
    if in_paragraph:
        html_lines.append("</p>")
    return html_lines


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
            lines = [line.strip('\n') for line in f]
            processed_lines = []
            in_list = False
            list_type = None
            for line in lines:
                line = parse_special_syntax(line)
                line = parse_bold_and_emphasis(line)
                processed_line, in_list, list_type = parse_list(parse_heading(line), in_list, list_type)
                processed_lines.append(processed_line)
            processed_lines = parse_paragraphs(processed_lines)
            with open(html_file, 'w') as html:
                for line in processed_lines:
                    html.write(line + '\n')
                if in_list:
                    html.write(f"</{list_type}>\n")
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
