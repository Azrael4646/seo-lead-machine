import re

def find_email(html):

    email_regex = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

    emails = re.findall(email_regex, html.lower())

    return list(set(emails))
