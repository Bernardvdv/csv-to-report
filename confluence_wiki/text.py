import re

from utils import enclosed_tag


# Rules taken from: https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all
bold_rule = re.compile('(\*.*?\*)')
heading_rule = re.compile('(h[1-6].*)')


def parse_bold(source):
    # Characters wrapped in *strong*
    for match in bold_rule.findall(source):
        cleaned_string = match.replace("*", "")
        tag = enclosed_tag("b", cleaned_string)
        source = source.replace(match, tag)
        # source = source.replace(match, cleaned_string)
    return source


def parse_heading(source):
    # Words starting with: "h1.", "h2.", "h3.", "h4.", "h5." or "h6."
    for match in heading_rule.findall(source):
        heading_number = match[1]
        cleaned_string = match.replace(f"h{heading_number}. ", "")
        # source = source.replace(match, cleaned_string)
        tag = enclosed_tag("b", cleaned_string)
        source = source.replace(match, tag)
    return source
