import concurrent.futures
from audit import audit_site

MAX_WORKERS = 20

def audit_many(websites):

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        future_to_site = {
            executor.submit(audit_site, site): site for site in websites
        }

        for future in concurrent.futures.as_completed(future_to_site):

            site = future_to_site[future]

            try:
                score, issues, data = future.result()

                results.append({
                    "website": site,
                    "seo_score": score,
                    "pages_crawled": data.get("pages_crawled", 0),
                    "issues": ", ".join(issues)
                })

            except Exception as e:

                results.append({
                    "website": site,
                    "seo_score": 0,
                    "pages_crawled": 0,
                    "issues": "Audit failed"
                })

    return results
