from ddgs import DDGS

def find_activities(destination:str):
    query = f"find best activites to do in {destination}"

    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results = 5)

        for result in search_results:
            results.append({
                "name":result["name"],
                "link":result["link"],
                "description":result["body"],
            })

    return results