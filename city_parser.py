import re

def parseBracketStyle(title):
    if title:
	m = re.match(r".*\[(.*?)\]", title);
	if m:
	    return m.group(1);
