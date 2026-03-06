import requests
from bs4 import BeautifulSoup

def audit_site(url):

    issues = []

    r = requests.get(url, timeout=10)

    html = r.text

    soup = BeautifulSoup(html,"html.parser")

    if not soup.title:
        issues.append("Missing title tag")

    if not soup.find("meta",attrs={"name":"description"}):
        issues.append("Missing meta description")

    h1 = soup.find_all("h1")

    if len(h1) == 0:
        issues.append("No H1 tag")

    images = soup.find_all("img")

    missing_alt = [img for img in images if not img.get("alt")]

    if len(missing_alt) > 3:
        issues.append("Images missing alt text")

    score = 100 - (len(issues)*15)

    return score, issues, html
