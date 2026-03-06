from serpapi import GoogleSearch

API_KEY = "c30fa9eba310d387d6953d32f3bc0ee2481b2bead3c29c42f806fcf2bc532423"

def get_maps_leads(query):

    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    leads = []

    if "local_results" in results:

        for place in results["local_results"]:

            leads.append({
                "business": place.get("title"),
                "address": place.get("address"),
                "phone": place.get("phone"),
                "rating": place.get("rating"),
                "website": place.get("website")
            })

    return leads
