from ddgs import DDGS

def find_transport(route: str):
    query = f"Find transport options {route} flights train bus travel time"

    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results = 5)

        for result in search_results:
            results.append({
                "name":result["name"],
                "link":result["link"],
                "description":result["body"]
            })

    return results