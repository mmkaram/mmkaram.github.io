'''Converts markdown to HTML'''
# Mahdy Karam 2024-01
# With the [^1] footnote syntax

import sys
import os
import re

def convert():
    '''goes through the markdown file and converts it to HTML based on my setup'''
    if len(sys.argv) != 3:
        print("Usage: python3 MDToHTML.py [input file] [output file]")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print(f"File {sys.argv[1]} does not exist.")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding='utf-8') as f:
        lines = f.readlines()
    with open(sys.argv[2], "w", encoding='utf-8') as f:
        f.write("<!DOCTYPE html>")
        f.write("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")

        # Extract filename from the path
        filename = os.path.basename(sys.argv[1])

        # Remove .md extension
        title = os.path.splitext(filename)[0]

        f.write("<html>\n")
        f.write("<head>\n")
        f.write(f"<title>{title}</title>\n")
        f.write("<link rel=\"stylesheet\" href=\"all.css\">\n")
        f.write("<link rel=\"icon\" href=\"icon.ico\">")

        # script tag for copyright footer
        f.write("<script> document.addEventListener('DOMContentLoaded', function() {var currentYear = new Date().getFullYear(); var footerYear = document.getElementById('footer-year');footerYear.textContent = currentYear;});</script>")

        f.write("</head>\n")
        f.write("<body>\n")
        # f.write("<div class=\"header\">")
        # f.write("<h1></h1>")
        # f.write("</div>")
        f.write("<div class=\"main-content\">")
        f.write("<p><a href=\"index.html\">home</a></p>")
        f.write("<div>")
        f.write("</div><p>")

        for line in lines:

            line = line.replace("\n", "<br>")
            line = line.replace("\r", "")

            bold_pattern = r'\*\*([^\*]+)\*\*'
            line = re.sub(bold_pattern, r'<b>\1</b>', line)

            italic_pattern = r'\*([^\*]+)\*'
            line = re.sub(italic_pattern, r'<i>\1</i>', line)

            img_pattern = r'!\[([^\]]+)\]\(([^\)]+)\)'
            line = re.sub(img_pattern, r'<img src="\2" alt="\1">', line)

            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            line = re.sub(link_pattern, r'<a href="\2">\1</a>', line)

            footnote_text_pattern = r'\[\^(\d+)\]: (.*)'
            line = re.sub(footnote_text_pattern, r'<p><sup id="note\1">\1. <a href="#ref\1">↩</a></sup> \2</p>', line)
            
            footnote_ref_pattern = r'\[\^(\d+)\]'
            line = re.sub(footnote_ref_pattern, r'<sup id="ref\1"><a href="#note\1">\1</a></sup>', line)

            if line.startswith('> '):
                line = '<blockquote>' + line[2:] + '</blockquote>'

            list_pattern = r'^[\t ]*- (.*)$'
            line = re.sub(list_pattern, r'<li>\1</li>', line)

            inline_code_pattern = r'`+([^`]+)`+'
            line = re.sub(inline_code_pattern, r'<code>\1</code>', line)

            if line.startswith('# '):
                line = '<h1>' + line[2:] + '</h1>'
            elif line.startswith('## '):
                line = '<h2>' + line[3:] + '</h2>'
            elif line.startswith('### '):
                line = '<h3>' + line[4:] + '</h3>'
            elif line.startswith('#### '):
                line = '<h4>' + line[5:] + '</h4>'
            elif line.startswith('##### '):
                line = '<h5>' + line[6:] + '</h5>'
            elif line.startswith('###### '):
                line = '<h6>' + line[7:] + '</h6>'

            f.write(line + "\n")
        f.write("<footer>&copy; <span id=\"footer-year\"></span> Mahdy M. Karam</footer>")
        f.write("</p></body>\n</html>")

convert()
