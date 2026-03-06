import re

def find_email(html):

    if not html:
        return []

    if not isinstance(html, str):
        return []

    email_regex = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

    emails = re.findall(email_regex, html.lower())

    return list(set(emails))
