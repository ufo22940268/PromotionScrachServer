from bs4 import NavigableString

def getStrings(node):
    if isinstance(node, NavigableString):
        return node.string.strip().encode("utf-8");
    else:
        return "".join(node.strings).encode("utf-8");
