# Module for translating simple Markdown formatted text to HTML
# It supports:
# - headings
# - bold, italic text
# - unordered and ordered lists
# - links
# - paragraphs

import re

# Common

def is_line_contains(line: str, items: list) -> bool:
    for i in items:
        if i in line:
            return True
    return False

# Heading functions

def check_heading(line: str):
    headings = {
        "######": "h6",
        "#####": "h5",
        "####": "h4",
        "###": "h3",
        "##": "h2",
        "#": "h1"
    }

    for heading in headings:
        if heading in line:
            return headings[heading]

def convert_heading(line: str, heading: str) -> str:
    headings = {
        "h1": "#",
        "h2": "##",
        "h3": "###",
        "h4": "####",
        "h5": "#####",
        "h6": "#######"
    }
    assert heading in headings

    stripped_line = line.strip(headings[heading])
    return f"<{heading}>{stripped_line}</{heading}>\n\n"


# Bold & Italic check

def add_formatting_to_paragraph(paragraph: str) -> str:
    # Find all opening/closing bold & italic
    p = re.compile(r"\*\*\*(?P<text>[^'']+?)\*\*\*", re.S)
    paragraph = p.sub("<strong><em>\g<text></em></strong>", paragraph)

    # Find all opening/closing bold
    p = re.compile(r"\*\*(?P<text>[^'']+?)\*\*", re.S)
    paragraph = p.sub("<strong>\g<text></strong>", paragraph)

    # Find all opening/closing italic
    p = re.compile(r"\*(?P<text>[^'']+?)\*", re.S)
    paragraph = p.sub("<em>\g<text></em>", paragraph)

    return paragraph

# Links

def transform_link(line: str) -> str:
    p = re.compile(r"\[(?P<name>.+?)\]\((?P<url>.+?)\)")
    line = p.sub("<a href='\g<url>'>\g<name></a>", line)
    return line

# Unordered lists

def check_line_is_list(line: str) -> bool:
    return (line.startswith("- ") or line.startswith("* "))

def create_list(l: str) -> str:
    splitted_list = l.split("\n")
    empty_str_filtered = filter(None, splitted_list)
    html = "<ul>\n"
    for line in empty_str_filtered:
        html += f"<li>{line[2:]}</li>\n"
    html += "</ul>\n\n"
    return html

# Ordered lists

def check_line_is_ol(line: str) -> bool:
    p = re.compile(r"\d\. (?P<item>.+)")
    return p.match(line)

def create_ol(l: str) -> str:
    splitted_list = l.split("\n")
    empty_str_filtered = filter(None, splitted_list)
    html = "<ol>\n"
    for line in empty_str_filtered:
        html += f"<li>{line[3:]}</li>\n"
    html += "</ol>\n\n"
    return html

# Paragraph function

def add_paragraph(line: str, start: bool) -> str:
    if start:
        return f"<p>{line}"
    else:
        return f"{line}</p>"

# Main

def process_md(md: str) -> str:

    md_lines = md.split("\n")

    html_lines = []
    paragraph = ""
    ul = ""
    ol = ""

    for line in md_lines:

        # Check for heading
        found_heading = check_heading(line)
        if found_heading:
            l = convert_heading(line, found_heading)
            html_lines.append(l)
            continue

        # Unordered list check

        if check_line_is_list(line):
            ul += f"{line}\n"
            continue
        else:
            if ul:
                html_lines.append(create_list(ul))
                ul = ""

        # Ordered list check

        if check_line_is_ol(line):
            ol += f"{line}\n"
            continue
        else:
            if ol:
                html_lines.append(create_ol(ol))
                ol = ""

        # URL check

        line = transform_link(line)

        # Paragraph check

        # If paragraph started
        if paragraph:
            # If blank line - close paragraph, append and make paragraph empty
            if line == "":
                paragraph += "</p>\n\n"
                paragraph = add_formatting_to_paragraph(paragraph)
                html_lines.append(paragraph)
                paragraph = ""
                continue
            else:
                paragraph += f"{line}\n"
                continue
        else:
            # Open paragraph
            paragraph += f"<p>{line}"
            continue
    
    # Check if have started paragraph, ul or ol
    if ul:
        html_lines.append(create_list(ul))

    if ol:
        html_lines.append(create_ol(ol))

    if paragraph:
        paragraph += "</p>\n\n"
        paragraph = add_formatting_to_paragraph(paragraph)
        html_lines.append(paragraph)

    return "".join(html_lines)
