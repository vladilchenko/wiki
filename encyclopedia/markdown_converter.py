# headings, boldface text, unordered lists, links, and paragraphs

import re


text = """
#Main heading
## Sub heading
### Sub sub heading
**This should be bold**
*this should be italic*
___This is bold AND italic___
[Some link](https://google.com)

######Small heading
- list_item1
- list_item1
- list_item1

#####H5 heading
1. Ordered item
2. Ordered item2
3. Ordered item3

Paragraph1Paragraph1Paragraph1*Paragraph1*Paragraph1**Parag*raph1**Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1
Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1Paragraph1


Paragraph2Paragraph2Paragraph2**Paragraph**2Paragraph2Paragraph2
Paragraph2**Paragraph2Paragraph2Paragraph2Paragraph2Paragraph2Paragraph2
Paragraph2*Paragraph2Paragraph2Paragraph2Paragraph2Paragraph2Paragraph2Paragraph2Paragraph2
"""

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

    for line in md_lines:

        # Check for heading
        found_heading = check_heading(line)
        if found_heading:
            l = convert_heading(line, found_heading)
            html_lines.append(l)
            continue

        # Bold Italic check




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
    
    return "".join(html_lines)

print(process_md(text))
