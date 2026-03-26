from ddgs import DDGS

def find_hotels(destination: str):
    query = f"Find best hotels or stay option in {destination}"
    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results = 5)
        for result in search_results:
            results.append({
                "name":result["title"],
                "link":result["href"],
                "description":result["body"],
            })

    return results
