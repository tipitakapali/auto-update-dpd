import urllib.parse
import html
import re

"""Get the feedback word id for google form"""


def extract_text_from_div(html_content, find_re):
    # Define the regex pattern to match the specific div tag and capture its content
    match = re.search(find_re, html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return ""


def extract_feedback_word_id(
    html_content, find_re, start_pattern="entry.438735500=", end_pattern="&entry"
):
    selected_text = extract_text_from_div(html_content, find_re)
    if not selected_text:
        return ""
    decoded_url = urllib.parse.unquote(selected_text)
    fully_decoded_url = html.unescape(decoded_url)
    pattern = re.escape(start_pattern) + "(.*?)" + re.escape(end_pattern)
    match = re.search(pattern, fully_decoded_url)
    if match:
        return match.group(1)
    else:
        return ""

