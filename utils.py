

def open_tag(tag):
    return f"<{tag}>\n"


def enclosed_tag(tag, string):
    return f"<{tag}>{string}</{tag}>\n"


def close_tag(tag):
    return f"</{tag}>\n"
