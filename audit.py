import requests
from bs4 import BeautifulSoup
import time

def audit_site(url):

    issues = []
    data = {}

    # Ensure schema exists
    if not url.startswith("http"):
        url = "https://" + url

    try:

        start = time.time()
        r = requests.get(url, timeout=10)
        load_time = time.time() - start

        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        # ------------------------
        # Basic Technical Checks
        # ------------------------

        if not url.startswith("https"):
            issues.append("Site not using HTTPS")

        if load_time > 3:
            issues.append("Slow page load (>3s)")

        data["load_time"] = round(load_time,2)

        # ------------------------
        # Title Tag
        # ------------------------

        title = soup.title.string.strip() if soup.title else ""

        if not title:
            issues.append("Missing title tag")
        elif len(title) < 30 or len(title) > 60:
            issues.append("Title length not optimal (30-60 chars)")

        data["title"] = title

        # ------------------------
        # Meta Description
        # ------------------------

        meta_desc = soup.find("meta", attrs={"name":"description"})

        if not meta_desc:
            issues.append("Missing meta description")
            desc_text = ""
        else:
            desc_text = meta_desc.get("content","")
            if len(desc_text) < 70 or len(desc_text) > 160:
                issues.append("Meta description length not optimal")

        data["meta_description"] = desc_text

        # ------------------------
        # Headings
        # ------------------------

        h1_tags = soup.find_all("h1")

        if len(h1_tags) == 0:
            issues.append("Missing H1 tag")

        if len(h1_tags) > 1:
            issues.append("Multiple H1 tags")

        data["h1_count"] = len(h1_tags)

        # ------------------------
        # Word Count
        # ------------------------

        text = soup.get_text(separator=" ")
        words = text.split()

        if len(words) < 300:
            issues.append("Low content word count")

        data["word_count"] = len(words)

        # ------------------------
        # Images
        # ------------------------

        images = soup.find_all("img")
        missing_alt = [img for img in images if not img.get("alt")]

        if len(images) > 0 and len(missing_alt) / len(images) > 0.3:
            issues.append("Many images missing alt text")

        data["images"] = len(images)
        data["missing_alt"] = len(missing_alt)

        # ------------------------
        # Internal Links
        # ------------------------

        links = soup.find_all("a", href=True)
        internal_links = [l for l in links if url in l["href"]]

        if len(internal_links) < 3:
            issues.append("Very few internal links")

        data["internal_links"] = len(internal_links)

        # ------------------------
        # Canonical Tag
        # ------------------------

        canonical = soup.find("link", rel="canonical")

        if not canonical:
            issues.append("Missing canonical tag")

        # ------------------------
        # Viewport (Mobile SEO)
        # ------------------------

        viewport = soup.find("meta", attrs={"name":"viewport"})

        if not viewport:
            issues.append("Missing mobile viewport tag")

        # ------------------------
        # Structured Data
        # ------------------------

        schema = soup.find_all("script", type="application/ld+json")

        if not schema:
            issues.append("No structured data (Schema.org)")

        data["schema_blocks"] = len(schema)

        # ------------------------
        # Robots Meta
        # ------------------------

        robots_meta = soup.find("meta", attrs={"name":"robots"})

        if robots_meta and "noindex" in robots_meta.get("content",""):
            issues.append("Page is set to noindex")

        # ------------------------
        # Sitemap Check
        # ------------------------

        try:
            sitemap = requests.get(url + "/sitemap.xml", timeout=5)

            if sitemap.status_code != 200:
                issues.append("No sitemap.xml found")
        except:
            issues.append("Sitemap not accessible")

        # ------------------------
        # Robots.txt Check
        # ------------------------

        try:
            robots = requests.get(url + "/robots.txt", timeout=5)

            if robots.status_code != 200:
                issues.append("No robots.txt found")
        except:
            issues.append("robots.txt not accessible")

        # ------------------------
        # Score Calculation
        # ------------------------

        score = max(0, 100 - len(issues)*5)

        return score, issues, data

    except Exception as e:

        return 0, ["Site unreachable"], {}
