# Mahdy Karam 2024-01
# Converts markdown to HTML
# With the [^1] footnote syntax

import sys
import os
import re

def convert():
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

        
        f.write("<html>\n")
        f.write("<head>\n")
        f.write("<link href='https://fonts.googleapis.com/css?family=League Spartan' rel='stylesheet'>")
        f.write("<link rel=\"stylesheet\" href=\"all.css\">\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<div class=\"header\">")
        f.write("<h1></h1>")
        f.write("</div>")
        f.write("<div class=\"main-content\">")
        f.write("<p><a href=\"index.html\">home</a></p>")
        f.write("<div>")
        f.write("<h1> Squash AI</h1>")
        f.write("</div>")

        code_flag = False
        for line in lines:

            line = line.replace("\n", "</p><p>")
            line = line.replace("\r", "")

            bold_pattern = r'\*\*([^\*]+)\*\*'
            line = re.sub(bold_pattern, r'<b>\1</b>', line)

            italic_pattern = r'\*([^\*]+)\*'
            line = re.sub(italic_pattern, r'<i>\1</i>', line)

            img_pattern = r'!\[([^\]]+)\]\(([^\)]+)\)'
            line = re.sub(img_pattern, r'<img src="\2" alt="\1">', line)

            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            line = re.sub(link_pattern, r'<a href="\2">\1</a>', line)

            footnote_ref_pattern = r'\[\^(\d+)\]'
            line = re.sub(footnote_ref_pattern, r'<sup id="ref\1"><a href="#note\1">\1</a></sup>', line)

            footnote_text_pattern = r'\[\^(\d+)\]: (.*)'
            line = re.sub(footnote_text_pattern, r'<p id="note\1">\1. <a href="#ref\1">↩</a> \2</p>', line)

            if line.startswith('> '):
                line = '<blockquote>' + line[2:] + '</blockquote>'

            if "```" in line:
                if not code_flag:
                    line = line.replace("```", "<code>")
                    code_flag = True
                else:
                    line = line.replace("```", "</code>")
                    code_flag = False
            
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
        f.write("</body>\n</html>")
convert()
